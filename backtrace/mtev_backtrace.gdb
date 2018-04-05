source luajit21.py
set $ck_hs_map = mtev_coros.u.hs.map
set $n = $ck_hs_map.n_entries
set $i = 0
while($ck_hs_map.entries[$i] == 0)
  set $i = $i + 1
end
set $ck_hs_map_cursor = $ck_hs_map.entries[$i]

set $ck_hs_attr = (struct ck_hash_attr *)(void *)(((char *)$ck_hs_map_cursor) - ((size_t)&((struct ck_hash_attr *)0)->key))
set $ck_hs_key = $ck_hs_attr.key_ptr

set $L = ((lua_State **)$ck_hs_key)[0]
printf "\n"
lbt $L

