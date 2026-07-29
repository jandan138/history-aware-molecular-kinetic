#pragma once

#include <deque>

#include "historykinetic/types.hpp"

namespace hamk {

class CollisionHistoryWindow {
public:
    explicit CollisionHistoryWindow(double duration);

    void push(CollisionEvent event);
    void expire(double now);
    [[nodiscard]] CollisionGraphSummary summarize() const;
    [[nodiscard]] std::size_t size() const noexcept { return events_.size(); }

private:
    double duration_;
    std::deque<CollisionEvent> events_;
};

}  // namespace hamk
