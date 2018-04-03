local print = print
local ffi = require("ffi")
local mtev = require("mtev")

module(...)

local function B()
  local p = ffi.cast("int*", 0xdeadbeef)
  print(p[0])
end

function main()
  print("reading bad memory..")
  local A = function() B() end
  A()
end
