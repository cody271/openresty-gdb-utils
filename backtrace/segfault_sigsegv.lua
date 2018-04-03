local ffi = require("ffi")
ffi.cdef([[
typedef int (*sigsegv_handler_t) (void* fault_address, int serious);
extern int sigsegv_install_handler (sigsegv_handler_t handler);
]])
ffi.load("sigsegv").sigsegv_install_handler(function(addr, srsly)
  print(debug.traceback())
  os.exit()
end)

local function B()
  local p = ffi.cast("int*", 0xdeadbeef)
  print(p[0])
end

function main()
  print("reading bad memory..")
  local A = function() B() end
  A()
end

main()
