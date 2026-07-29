#pragma once

#include <array>
#include <cstdint>
#include <string>

namespace hamk {

using Vec3 = std::array<double, 3>;

struct CollisionEvent {
    double time{};
    std::uint64_t particle_a{};
    std::uint64_t particle_b{};
    std::string block_id;
    Vec3 pre_velocity_a{};
    Vec3 pre_velocity_b{};
    Vec3 post_velocity_a{};
    Vec3 post_velocity_b{};
};

struct CollisionGraphSummary {
    std::size_t collision_count{};
    std::size_t unique_pair_count{};
    double repeated_pair_ratio{};
    std::size_t vertex_count{};
    std::size_t component_count{};
    std::size_t cycle_rank{};
    double largest_component_fraction{};
};

}  // namespace hamk
