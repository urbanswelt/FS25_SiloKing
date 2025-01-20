-- Check if the script has already been executed
if _G.myScriptExecuted then
    return
end

-- Mark the script as executed
_G.myScriptExecuted = true


-- Retrieve the global environment and metatable
local globalEnvironment = _G
local globalEnvironmentMetatable = getmetatable(_G)
if globalEnvironmentMetatable then
    globalEnvironment = Utils.getNoNil(globalEnvironmentMetatable.__index, _G)
end

-- Reference the Utils module
local utilsModule = globalEnvironment["Utils"]
if utilsModule then
    local originalGetFilename = utilsModule.getFilename

    -- Overwrite the getFilename function
    utilsModule.getFilename = function(inputFilename, basePath, ...)
        if type(inputFilename) ~= "string" then
            return originalGetFilename(inputFilename, basePath, ...)
        end

        -- Extract prefix if present
        local _, endPosition, prefix = inputFilename:find("^%$([%w_]+)%$")
        if not prefix then
            return originalGetFilename(inputFilename, basePath, ...)
        end

        local remainingFilename = inputFilename:sub(endPosition + 1)
        local prefixLowercase = prefix:lower()
        local isModRequired = true

        -- Handle special prefixes
        if remainingFilename:sub(1, 1) == "!" then
            remainingFilename = remainingFilename:sub(2)
            isModRequired = false
        end

        if remainingFilename:sub(1, 1) == "/" then
            remainingFilename = remainingFilename:sub(2)
        end

        if prefixLowercase == "mapdir" then
            if g_currentMission and g_currentMission.missionInfo then
                local mapDirectory = g_currentMission.missionInfo.baseDirectory
                if Utils.getNoNil(mapDirectory, "") ~= "" then
                    return originalGetFilename(remainingFilename, mapDirectory)
                end
            end
        elseif g_modManager and g_modIsLoaded then
            local modInfo = nil

            -- Handle mod-specific prefixes
            if prefixLowercase == "moddir" or prefixLowercase == "pdlcdir" then
                local firstSlashPosition = remainingFilename:find("/")
                if firstSlashPosition and firstSlashPosition > 1 then
                    local modName = remainingFilename:sub(1, firstSlashPosition - 1)

                    if modName and prefixLowercase == "pdlcdir" and g_dlcModNameHasPrefix[modName] then
                        modName = g_uniqueDlcNamePrefix .. modName
                    end

                    modInfo = g_modManager:getModByName(modName)
                    if modInfo then
                        remainingFilename = remainingFilename:sub(firstSlashPosition + 1)
                    end
                end
            else
                modInfo = g_modManager:getModByName(prefix)
            end

            if modInfo and (not isModRequired or g_modIsLoaded[modInfo.modName]) then
                return originalGetFilename(remainingFilename, modInfo.modDir)
            end
        end

        return originalGetFilename(inputFilename, basePath, ...)
    end
end
