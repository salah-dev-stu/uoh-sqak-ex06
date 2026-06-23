# Mechanism PRD — Game Engine

**Modules:** `domain/{geometry,grid,pieces,actions,observation,rules,terminal,scoring,state,records}`

Pure, IO-free game logic. 2D grid (default 5×5, config-driven), 8-direction movement
incl. diagonals, no wrapping. Sub-game ≤25 moves, thief moves first. Cop may place
≤5 barriers instead of moving; barriers block both agents and are fatal to enter.
Win: cop shares thief's cell (cop +20/thief +5) or thief survives (thief +10/cop +5)
— scores from config. Partial observability via Chebyshev `vision_radius`. State
transitions are immutable (`apply` returns a new state). `MoveRecord`/`SubGameResult`/
`GameResult` are the dispute-evidence log shapes. **Gates:** H5, H6.
