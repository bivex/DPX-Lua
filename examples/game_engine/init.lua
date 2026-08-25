-- DPX-Lua Example Game Engine
local M = {}

M.version = "1.0.0"

local Player = require("player")
local ParticlePool = require("particle_pool")

function M.create_game()
    local player = Player.new("Hero")
    local pool = ParticlePool.new(100)
    return {
        player = player,
        pool = pool,
    }
end

return M
