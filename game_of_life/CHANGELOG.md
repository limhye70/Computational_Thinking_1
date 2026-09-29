# Changelog

All notable changes to this project will be documented in this file.

## [Week 2]
### Changed
- The entire cells are not calculated every generation.
- Instead, we use a lookup table (hashmap) which contain every possible m-by-m bloc and its next generations.
- The input matrix is sliced into m-by-m blocks and each block refers the table to obtain its next generation. 
### Notes
- Running time dropped by 77% (~390 to ~90 secs)
- Try to replace loops for efficiency. e.g., adding zero-rows/cols at once instead of one-by-one

## [Week 1] - 2026-09-25
### Added
- Initial Game of Life implementation using brute-force neighbor checking
- Baseline solution