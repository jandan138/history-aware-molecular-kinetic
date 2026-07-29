#pragma once

#include <filesystem>
#include <string>
#include <vector>

namespace hamk {

class ISolverBackend {
public:
    virtual ~ISolverBackend() = default;
    [[nodiscard]] virtual std::string name() const = 0;
    virtual void validate_case(const std::filesystem::path& case_file) const = 0;
    virtual std::vector<std::filesystem::path> run(
        const std::filesystem::path& case_file,
        const std::filesystem::path& run_directory) = 0;
};

[[nodiscard]] std::string native_contract_version();

}  // namespace hamk
