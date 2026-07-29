#include <cassert>

#include "historykinetic/history_window.hpp"
#include "historykinetic/solver.hpp"

namespace {

hamk::CollisionEvent event(double time, std::uint64_t a, std::uint64_t b) {
    hamk::CollisionEvent value{};
    value.time = time;
    value.particle_a = a;
    value.particle_b = b;
    value.block_id = "b0";
    return value;
}

}  // namespace

int main() {
    assert(hamk::native_contract_version() == "0.1.0");

    hamk::CollisionHistoryWindow window(10.0);
    window.push(event(0.0, 0, 1));
    window.push(event(1.0, 1, 2));
    window.push(event(2.0, 2, 0));
    const auto summary = window.summarize();
    assert(summary.collision_count == 3);
    assert(summary.cycle_rank == 1);
    assert(summary.component_count == 1);
    return 0;
}
