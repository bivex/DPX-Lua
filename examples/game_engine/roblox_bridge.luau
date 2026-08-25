-- Luau Roblox Network Bridge
export type NetworkPacket = {
    event_id: string,
    payload: string,
}

local function sync_network(packet: NetworkPacket)
    local ReplicatedStorage = game:GetService("ReplicatedStorage")
    local RemoteEvent = ReplicatedStorage.SyncPacket
    RemoteEvent:FireServer(packet.event_id, packet.payload)
end

return {
    sync_network = sync_network
}
