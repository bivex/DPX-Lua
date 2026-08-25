local ParticlePool = {}
ParticlePool.__index = ParticlePool

function ParticlePool.new(capacity)
    local self = setmetatable({}, ParticlePool)
    self.pool = table.create(capacity)
    return self
end

function ParticlePool:spawn(x, y)
    local p = { x = x, y = y }
    table.insert(self.pool, p)
    return p
end

return ParticlePool
