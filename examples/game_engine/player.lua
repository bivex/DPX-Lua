local Player = {}
Player.__index = Player

function Player.new(name)
    local self = setmetatable({}, Player)
    self.name = name
    self.health = 100
    self.x = 0
    self.y = 0
    return self
end

function Player:set_position(x, y)
    self.x = x
    self.y = y
    return self
end

function Player:update(dt)
    self:on_before_update(dt)
    -- Frame yield in cooperative coroutine
    coroutine.yield(self.x)
end

function Player:on_before_update(dt)
end

function Player:subscribe(fn)
    table.insert(self.listeners, fn)
end

return Player
