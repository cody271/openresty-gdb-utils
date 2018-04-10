import gdb

#
# ck_hs_t* keys -> (entries)
#
def ck_hs_keys(ck_hs):
    ck_hs_map = ck_hs["map"]
    capacity = int(ck_hs_map["capacity"])
    n_entries = int(ck_hs_map["n_entries"])
    entries = []
    for i in range(capacity):
        entry = int(ck_hs_map["entries"][i])
        if entry != 0:
            entries.append(entry)
    assert len(entries) == n_entries
    return tuple(entries)

#
# dereference lua_State**
#
def Lptr(L):
    Lptr_expr = "((lua_State **)0x%x)[0]" % L
    return gdb.parse_and_eval(Lptr_expr)

#
# ck_hs_t* entry -> ck_hash_attr_t* (mtev_hash.h)
#
_CK_CC_CONTAINER_expr = "(ck_hash_attr_t *)(void *)(((char *)0x%x) - ((size_t)&((ck_hash_attr_t *)0)->key))"
def index_attribute_container(entry):
    entry_expr = _CK_CC_CONTAINER_expr % entry
    return gdb.parse_and_eval(entry_expr)

#
# ck_hs_t* entry -> lua_State*
#
def ck_hs_entry_to_L(entry):
    mtev_entry = index_attribute_container(entry)
    key_ptr = mtev_entry["key_ptr"]
    return Lptr(key_ptr)

#
# mtev_hash_table* -> ck_hs_t*
#
def mtev_to_ck_hs(mtev_ht):
    return mtev_ht["u"]["hs"]

#
# "symbol" (mtev_hash_table*) -> (L)
#
def mtev_L(sym_mtev_ht):
    mtev_ht, _ = gdb.lookup_symbol(sym_mtev_ht)
    assert mtev_ht, "Failed to load symbol: %s" % sym_mtev_ht
    ck_hs = mtev_to_ck_hs(mtev_ht.value())
    ck_keys = ck_hs_keys(ck_hs)
    return tuple(map(ck_hs_entry_to_L, ck_keys))

