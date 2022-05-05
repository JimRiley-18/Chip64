import chip64
code = [
# data section
    0x10, 0x0A, # jump to main
# 4 million $2
    0x0, 0x0,
    0x0, 0x0,
    0x0, 0x3d,
    0x09, 0x00,
# main $10
    # name registers 0 -> lim
    #                1 -> b
    #                2 -> total
    #                3 -> tmp
    #                4 -> a
    0x64, 0x00, # a = 0
    0x61, 0x01, # b = 1
    0x62, 0x00, # total = 0
    0xA0, 0x02, # memory_ptr = 2
    0xE0, 0x65, # lim = 4'000'000
# loop_top $20
    # now testing if a < 4'000'000
    # sub a, lim gives carry of 0 means a < lim
    0x83, 0x40, # tmp = a
    0x83, 0x05, # tmp -= lim
    0x3F, 0x00, # skip next if carry is 0
    0x10, 0x2C, # jump to loop_end
    #check if a % 2 == 0
    0x83, 0x40, # tmp = a
    0x83, 0x16, # tmp >>= 1
    0x3F, 0x01, # skip next if carry is 1
    0x82, 0x44, # total += a
    0x83, 0x10, # tmp = b
    0x81, 0x44, # b += a
    0x84, 0x30, # a = tmp
    0x10, 0x14, # jump to loop_top
# loop_end $46
    0xD2, 0x01, # print(total)
    0x00, 0x00  # halt execution
]
c64 = chip64.Chip64(code)
c64.execute()
