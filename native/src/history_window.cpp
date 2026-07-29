#include "historykinetic/history_window.hpp"

#include <algorithm>
#include <map>
#include <set>
#include <stdexcept>
#include <unordered_map>
#include <utility>

namespace hamk {
namespace {

class DisjointSet {
public:
    void add(std::uint64_t value) {
        if (!parent_.contains(value)) {
            parent_[value] = value;
            size_[value] = 1;
        }
    }

    std::uint64_t find(std::uint64_t value) {
        auto root = value;
        while (parent_.at(root) != root) {
            root = parent_.at(root);
        }
        while (parent_.at(value) != value) {
            const auto next = parent_.at(value);
            parent_[value] = root;
            value = next;
        }
        return root;
    }

    void unite(std::uint64_t left, std::uint64_t right) {
        add(left);
        add(right);
        auto root_left = find(left);
        auto root_right = find(right);
        if (root_left == root_right) {
            return;
        }
        if (size_.at(root_left) < size_.at(root_right)) {
            std::swap(root_left, root_right);
        }
        parent_[root_right] = root_left;
        size_[root_left] += size_[root_right];
    }

    const std::unordered_map<std::uint64_t, std::uint64_t>& parent() const { return parent_; }

private:
    std::unordered_map<std::uint64_t, std::uint64_t> parent_;
    std::unordered_map<std::uint64_t, std::size_t> size_;
};

}  // namespace

CollisionHistoryWindow::CollisionHistoryWindow(double duration) : duration_(duration) {
    if (duration <= 0.0) {
        throw std::invalid_argument("duration must be positive");
    }
}

void CollisionHistoryWindow::push(CollisionEvent event) {
    if (!events_.empty() && event.time < events_.back().time) {
        throw std::invalid_argument("events must be time ordered");
    }
    events_.push_back(std::move(event));
    expire(events_.back().time);
}

void CollisionHistoryWindow::expire(double now) {
    const double cutoff = now - duration_;
    while (!events_.empty() && events_.front().time < cutoff) {
        events_.pop_front();
    }
}

CollisionGraphSummary CollisionHistoryWindow::summarize() const {
    if (events_.empty()) {
        return {};
    }

    using Pair = std::pair<std::uint64_t, std::uint64_t>;
    std::map<Pair, std::size_t> pair_counts;
    DisjointSet dsu;
    for (const auto& event : events_) {
        const auto pair = std::minmax(event.particle_a, event.particle_b);
        ++pair_counts[{pair.first, pair.second}];
        dsu.unite(event.particle_a, event.particle_b);
    }

    std::size_t repeated_events = 0;
    for (const auto& [pair, count] : pair_counts) {
        static_cast<void>(pair);
        if (count > 1) {
            repeated_events += count - 1;
        }
    }

    std::set<std::uint64_t> roots;
    std::map<std::uint64_t, std::size_t> component_sizes;
    auto mutable_dsu = dsu;
    for (const auto& [vertex, parent] : dsu.parent()) {
        static_cast<void>(parent);
        const auto root = mutable_dsu.find(vertex);
        roots.insert(root);
        ++component_sizes[root];
    }

    std::size_t largest = 0;
    for (const auto& [root, count] : component_sizes) {
        static_cast<void>(root);
        largest = std::max(largest, count);
    }

    const auto vertices = dsu.parent().size();
    const auto components = roots.size();
    const auto edges = pair_counts.size();
    const auto cycles = edges + components >= vertices ? edges - vertices + components : 0;

    return CollisionGraphSummary{
        .collision_count = events_.size(),
        .unique_pair_count = pair_counts.size(),
        .repeated_pair_ratio = static_cast<double>(repeated_events) /
                               static_cast<double>(events_.size()),
        .vertex_count = vertices,
        .component_count = components,
        .cycle_rank = cycles,
        .largest_component_fraction = static_cast<double>(largest) /
                                      static_cast<double>(vertices),
    };
}

}  // namespace hamk
