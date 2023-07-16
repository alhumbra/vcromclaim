#!/usr/bin/env python3


# Python re-implementation of https://github.com/mamedev/mame/blob/master/src/devices/bus/neogeo/prot_cmc.cpp (gfx part)
# but also with encryption, so that MAME can decrypt it

# WARNING: minor adjustments to the input and output maybe due to different "striping" of input data

#static const uint8_t kof2000_type0_t03[256] =
#{
kof2000_type0_t03 = [
	0x10, 0x61, 0xf1, 0x78, 0x85, 0x52, 0x68, 0xe3, 0x12, 0x0d, 0xfa, 0xf0, 0xc9, 0x36, 0x5e, 0x3d,
	0xf9, 0xa6, 0x01, 0x2e, 0xc7, 0x84, 0xea, 0x2b, 0x6d, 0x14, 0x38, 0x4f, 0x55, 0x1c, 0x9d, 0xa7,
	0x7a, 0xc6, 0xf8, 0x9a, 0xe6, 0x42, 0xb5, 0xed, 0x7d, 0x3a, 0xb1, 0x05, 0x43, 0x4a, 0x22, 0xfd,
	0xac, 0xa4, 0x31, 0xc3, 0x32, 0x76, 0x95, 0x9e, 0x7e, 0x88, 0x8e, 0xa2, 0x97, 0x18, 0xbe, 0x2a,
	0xf5, 0xd6, 0xca, 0xcc, 0x72, 0x3b, 0x87, 0x6c, 0xde, 0x75, 0xd7, 0x21, 0xcb, 0x0b, 0xdd, 0xe7,
	0xe1, 0x65, 0xaa, 0xb9, 0x44, 0xfb, 0x66, 0x15, 0x1a, 0x3c, 0x98, 0xcf, 0x8a, 0xdf, 0x37, 0xa5,
	0x2f, 0x67, 0xd2, 0x83, 0xb6, 0x6b, 0xfc, 0xe0, 0xb4, 0x7c, 0x08, 0xdc, 0x93, 0x30, 0xab, 0xe4,
	0x19, 0xc2, 0x8b, 0xeb, 0xa0, 0x0a, 0xc8, 0x03, 0xc0, 0x4b, 0x64, 0x71, 0x86, 0x9c, 0x9b, 0x16,
	0x79, 0xff, 0x70, 0x09, 0x8c, 0xd0, 0xf6, 0x53, 0x07, 0x73, 0xd4, 0x89, 0xb3, 0x00, 0xe9, 0xfe,
	0xec, 0x8f, 0xbc, 0xb2, 0x1e, 0x5d, 0x11, 0x35, 0xa9, 0x06, 0x59, 0x9f, 0xc1, 0xd3, 0x7b, 0xf2,
	0xc5, 0x77, 0x4e, 0x39, 0x20, 0xd5, 0x6a, 0x82, 0xda, 0x45, 0xf3, 0x33, 0x81, 0x23, 0xba, 0xe2,
	0x1d, 0x5f, 0x5c, 0x51, 0x49, 0xae, 0x8d, 0xc4, 0xa8, 0xf7, 0x1f, 0x0f, 0x34, 0x28, 0xa1, 0xd9,
	0x27, 0xd8, 0x4c, 0x2c, 0xbf, 0x91, 0x3e, 0x69, 0x57, 0x41, 0x25, 0x0c, 0x5a, 0x90, 0x92, 0xb0,
	0x63, 0x6f, 0x40, 0xaf, 0x74, 0xb8, 0x2d, 0x80, 0xbb, 0x46, 0x94, 0xe5, 0x29, 0xee, 0xb7, 0x1b,
	0x96, 0xad, 0x13, 0x0e, 0x58, 0x99, 0x60, 0x4d, 0x17, 0x26, 0xce, 0xe8, 0xdb, 0xef, 0x24, 0xa3,
	0x6e, 0x7f, 0x54, 0x3f, 0x02, 0xd1, 0x5b, 0x50, 0x56, 0x48, 0xf4, 0xbd, 0x62, 0x47, 0x04, 0xcd,
#};
]

#static const uint8_t kof2000_type0_t12[256] =
#{
kof2000_type0_t12 = [
	0xf4, 0x28, 0xb4, 0x8f, 0xfa, 0xeb, 0x8e, 0x54, 0x2b, 0x49, 0xd1, 0x76, 0x71, 0x47, 0x8b, 0x57,
	0x92, 0x85, 0x7c, 0xb8, 0x5c, 0x22, 0xf9, 0x26, 0xbc, 0x5b, 0x6d, 0x67, 0xae, 0x5f, 0x6f, 0xf5,
	0x9f, 0x48, 0x66, 0x40, 0x0d, 0x11, 0x4e, 0xb2, 0x6b, 0x35, 0x15, 0x0f, 0x18, 0x25, 0x1d, 0xba,
	0xd3, 0x69, 0x79, 0xec, 0xa8, 0x8c, 0xc9, 0x7f, 0x4b, 0xdb, 0x51, 0xaf, 0xca, 0xe2, 0xb3, 0x81,
	0x12, 0x5e, 0x7e, 0x38, 0xc8, 0x95, 0x01, 0xff, 0xfd, 0xfb, 0xf2, 0x74, 0x62, 0x14, 0xa5, 0x98,
	0xa6, 0xda, 0x80, 0x53, 0xe8, 0x56, 0xac, 0x1b, 0x52, 0xd0, 0xf1, 0x45, 0x42, 0xb6, 0x1a, 0x4a,
	0x3a, 0x99, 0xfc, 0xd2, 0x9c, 0xcf, 0x31, 0x2d, 0xdd, 0x86, 0x2f, 0x29, 0xe1, 0x03, 0x19, 0xa2,
	0x41, 0x33, 0x83, 0x90, 0xc1, 0xbf, 0x0b, 0x08, 0x3d, 0xd8, 0x8d, 0x6c, 0x39, 0xa0, 0xe3, 0x55,
	0x02, 0x50, 0x46, 0xe6, 0xc3, 0x82, 0x36, 0x13, 0x75, 0xab, 0x27, 0xd7, 0x1f, 0x0a, 0xd4, 0x89,
	0x59, 0x4f, 0xc0, 0x5d, 0xc6, 0xf7, 0x88, 0xbd, 0x3c, 0x00, 0xef, 0xcd, 0x05, 0x1c, 0xaa, 0x9b,
	0xed, 0x7a, 0x61, 0x17, 0x93, 0xfe, 0x23, 0xb9, 0xf3, 0x68, 0x78, 0xf6, 0x5a, 0x7b, 0xe0, 0xe4,
	0xa3, 0xee, 0x16, 0x72, 0xc7, 0x3b, 0x8a, 0x37, 0x2a, 0x70, 0xa9, 0x2c, 0x21, 0xf8, 0x24, 0x09,
	0xce, 0x20, 0x9e, 0x06, 0x87, 0xc5, 0x04, 0x64, 0x43, 0x7d, 0x4d, 0x10, 0xd6, 0xa4, 0x94, 0x4c,
	0x60, 0xde, 0xdf, 0x58, 0xb1, 0x44, 0x3f, 0xb0, 0xd9, 0xe5, 0xcb, 0xbb, 0xbe, 0xea, 0x07, 0x34,
	0x73, 0x6a, 0x77, 0xf0, 0x9d, 0x0c, 0x2e, 0x0e, 0x91, 0x9a, 0xcc, 0xc2, 0xb7, 0x63, 0x97, 0xd5,
	0xdc, 0xc4, 0x32, 0xe7, 0x84, 0x3e, 0x30, 0xa1, 0x1e, 0xb5, 0x6e, 0x65, 0xe9, 0xad, 0xa7, 0x96,
#};
]

#static const uint8_t kof2000_type1_t03[256] =
#{
kof2000_type1_t03 = [
	0x9a, 0x2f, 0xcc, 0x4e, 0x40, 0x69, 0xac, 0xca, 0xa5, 0x7b, 0x0a, 0x61, 0x91, 0x0d, 0x55, 0x74,
	0xcd, 0x8b, 0x0b, 0x80, 0x09, 0x5e, 0x38, 0xc7, 0xda, 0xbf, 0xf5, 0x37, 0x23, 0x31, 0x33, 0xe9,
	0xae, 0x87, 0xe5, 0xfa, 0x6e, 0x5c, 0xad, 0xf4, 0x76, 0x62, 0x9f, 0x2e, 0x01, 0xe2, 0xf6, 0x47,
	0x8c, 0x7c, 0xaa, 0x98, 0xb5, 0x92, 0x51, 0xec, 0x5f, 0x07, 0x5d, 0x6f, 0x16, 0xa1, 0x1d, 0xa9,
	0x48, 0x45, 0xf0, 0x6a, 0x9c, 0x1e, 0x11, 0xa0, 0x06, 0x46, 0xd5, 0xf1, 0x73, 0xed, 0x94, 0xf7,
	0xc3, 0x57, 0x1b, 0xe0, 0x97, 0xb1, 0xa4, 0xa7, 0x24, 0xe7, 0x2b, 0x05, 0x5b, 0x34, 0x0c, 0xb8,
	0x0f, 0x9b, 0xc8, 0x4d, 0x5a, 0xa6, 0x86, 0x3e, 0x14, 0x29, 0x84, 0x58, 0x90, 0xdb, 0x2d, 0x54,
	0x9d, 0x82, 0xd4, 0x7d, 0xc6, 0x67, 0x41, 0x89, 0xc1, 0x13, 0xb0, 0x9e, 0x81, 0x6d, 0xa8, 0x59,
	0xbd, 0x39, 0x8e, 0xe6, 0x25, 0x8f, 0xd9, 0xa2, 0xe4, 0x53, 0xc5, 0x72, 0x7e, 0x36, 0x4a, 0x4f,
	0x52, 0xc2, 0x22, 0x2a, 0xce, 0x3c, 0x21, 0x2c, 0x00, 0xd7, 0x75, 0x8a, 0x27, 0xee, 0x43, 0xfe,
	0xcb, 0x6b, 0xb9, 0xa3, 0x78, 0xb7, 0x85, 0x02, 0x20, 0xd0, 0x83, 0xc4, 0x12, 0xf9, 0xfd, 0xd8,
	0x79, 0x64, 0x3a, 0x49, 0x03, 0xb4, 0xc0, 0xf2, 0xdf, 0x15, 0x93, 0x08, 0x35, 0xff, 0x70, 0xdd,
	0x28, 0x6c, 0x0e, 0x04, 0xde, 0x7a, 0x65, 0xd2, 0xab, 0x42, 0x95, 0xe1, 0x3f, 0x3b, 0x7f, 0x66,
	0xd1, 0x8d, 0xe3, 0xbb, 0x1c, 0xfc, 0x77, 0x1a, 0x88, 0x18, 0x19, 0x68, 0x1f, 0x56, 0xd6, 0xe8,
	0xb6, 0xbc, 0xd3, 0xea, 0x3d, 0x26, 0xb3, 0xc9, 0x44, 0xdc, 0xf3, 0x32, 0x30, 0xef, 0x96, 0x4c,
	0xaf, 0x17, 0xf8, 0xfb, 0x60, 0x50, 0xeb, 0x4b, 0x99, 0x63, 0xba, 0xb2, 0x71, 0xcf, 0x10, 0xbe,
#};
]

#static const uint8_t kof2000_type1_t12[256] =
#{
kof2000_type1_t12 = [
	0xda, 0xa7, 0xd6, 0x6e, 0x2f, 0x5e, 0xf0, 0x3f, 0xa4, 0xce, 0xd3, 0xfd, 0x46, 0x2a, 0xac, 0xc9,
	0xbe, 0xeb, 0x9f, 0xd5, 0x3c, 0x61, 0x96, 0x11, 0xd0, 0x38, 0xca, 0x06, 0xed, 0x1b, 0x65, 0xe7,
	0x23, 0xdd, 0xd9, 0x05, 0xbf, 0x5b, 0x5d, 0xa5, 0x95, 0x00, 0xec, 0xf1, 0x01, 0xa9, 0xa6, 0xfc,
	0xbb, 0x54, 0xe3, 0x2e, 0x92, 0x58, 0x0a, 0x7b, 0xb6, 0xcc, 0xb1, 0x5f, 0x14, 0x35, 0x72, 0xff,
	0xe6, 0x52, 0xd7, 0x8c, 0xf3, 0x43, 0xaf, 0x9c, 0xc0, 0x4f, 0x0c, 0x42, 0x8e, 0xef, 0x80, 0xcd,
	0x1d, 0x7e, 0x88, 0x3b, 0x98, 0xa1, 0xad, 0xe4, 0x9d, 0x8d, 0x2b, 0x56, 0xb5, 0x50, 0xdf, 0x66,
	0x6d, 0xd4, 0x60, 0x09, 0xe1, 0xee, 0x4a, 0x47, 0xf9, 0xfe, 0x73, 0x07, 0x89, 0xa8, 0x39, 0xea,
	0x82, 0x9e, 0xcf, 0x26, 0xb2, 0x4e, 0xc3, 0x59, 0xf2, 0x3d, 0x9a, 0xb0, 0x69, 0xf7, 0xbc, 0x34,
	0xe5, 0x36, 0x22, 0xfb, 0x57, 0x71, 0x99, 0x6c, 0x83, 0x30, 0x55, 0xc2, 0xbd, 0xf4, 0x77, 0xe9,
	0x76, 0x97, 0xa0, 0xe0, 0xb9, 0x86, 0x6b, 0xa3, 0x84, 0x67, 0x1a, 0x70, 0x02, 0x5a, 0x41, 0x5c,
	0x25, 0x81, 0xaa, 0x28, 0x78, 0x4b, 0xc6, 0x64, 0x53, 0x16, 0x4d, 0x8b, 0x20, 0x93, 0xae, 0x0f,
	0x94, 0x2c, 0x3a, 0xc7, 0x62, 0xe8, 0xc4, 0xdb, 0x04, 0xc5, 0xfa, 0x29, 0x48, 0xd1, 0x08, 0x24,
	0x0d, 0xe2, 0xd8, 0x10, 0xb4, 0x91, 0x8a, 0x13, 0x0e, 0xdc, 0xd2, 0x79, 0xb8, 0xf8, 0xba, 0x2d,
	0xcb, 0xf5, 0x7d, 0x37, 0x51, 0x40, 0x31, 0xa2, 0x0b, 0x18, 0x63, 0x7f, 0xb3, 0xab, 0x9b, 0x87,
	0xf6, 0x90, 0xde, 0xc8, 0x27, 0x45, 0x7c, 0x1c, 0x85, 0x68, 0x33, 0x19, 0x03, 0x75, 0x15, 0x7a,
	0x1f, 0x49, 0x8f, 0x4c, 0xc1, 0x44, 0x17, 0x12, 0x6f, 0x32, 0xb7, 0x3e, 0x74, 0x1e, 0x21, 0x6a,
#};
]


#static const uint8_t kof2000_address_8_15_xor1[256] =
#{
kof2000_address_8_15_xor1 = [
	0xfc, 0x9b, 0x1c, 0x35, 0x72, 0x53, 0xd6, 0x7d, 0x84, 0xa4, 0xc5, 0x93, 0x7b, 0xe7, 0x47, 0xd5,
	0x24, 0xa2, 0xfa, 0x19, 0x0c, 0xb1, 0x8c, 0xb9, 0x9d, 0xd8, 0x59, 0x4f, 0x3c, 0xb2, 0x78, 0x4a,
	0x2a, 0x96, 0x9a, 0xf1, 0x1f, 0x22, 0xa8, 0x5b, 0x67, 0xa3, 0x0f, 0x00, 0xfb, 0xdf, 0xeb, 0x0a,
	0x57, 0xb8, 0x25, 0xd7, 0xf0, 0x6b, 0x0b, 0x31, 0x95, 0x23, 0x2d, 0x5c, 0x27, 0xc7, 0xf4, 0x55,
	0x1a, 0xf7, 0x74, 0xbe, 0xd3, 0xac, 0x3d, 0xc1, 0x7f, 0xbd, 0x28, 0x01, 0x10, 0xe5, 0x09, 0x37,
	0x1e, 0x58, 0xaf, 0x17, 0xf2, 0x16, 0x30, 0x92, 0x36, 0x68, 0xe6, 0xd4, 0xea, 0xb7, 0x75, 0x54,
	0x77, 0x41, 0xb4, 0x8d, 0xe0, 0xf3, 0x51, 0x03, 0xa9, 0xe8, 0x66, 0xab, 0x29, 0xa5, 0xed, 0xcb,
	0xd1, 0xaa, 0xf5, 0xdb, 0x4c, 0x42, 0x97, 0x8a, 0xae, 0xc9, 0x6e, 0x04, 0x33, 0x85, 0xdd, 0x2b,
	0x6f, 0xef, 0x12, 0x21, 0x7a, 0xa1, 0x5a, 0x91, 0xc8, 0xcc, 0xc0, 0xa7, 0x60, 0x3e, 0x56, 0x2f,
	0xe4, 0x71, 0x99, 0xc2, 0xa0, 0x45, 0x80, 0x65, 0xbb, 0x87, 0x69, 0x81, 0x73, 0xca, 0xf6, 0x46,
	0x43, 0xda, 0x26, 0x7e, 0x8f, 0xe1, 0x8b, 0xfd, 0x50, 0x79, 0xba, 0xc6, 0x63, 0x4b, 0xb3, 0x8e,
	0x34, 0xe2, 0x48, 0x14, 0xcd, 0xe3, 0xc4, 0x05, 0x13, 0x40, 0x06, 0x6c, 0x88, 0xb0, 0xe9, 0x1b,
	0x4d, 0xf8, 0x76, 0x02, 0x44, 0x94, 0xcf, 0x32, 0xfe, 0xce, 0x3b, 0x5d, 0x2c, 0x89, 0x5f, 0xdc,
	0xd2, 0x9c, 0x6a, 0xec, 0x18, 0x6d, 0x0e, 0x86, 0xff, 0x5e, 0x9e, 0xee, 0x11, 0xd0, 0x49, 0x52,
	0x4e, 0x61, 0x90, 0x0d, 0xc3, 0x39, 0x15, 0x83, 0xb5, 0x62, 0x3f, 0x70, 0x7c, 0xad, 0x20, 0xbf,
	0x2e, 0x08, 0x1d, 0xf9, 0xb6, 0xa6, 0x64, 0x07, 0x82, 0x38, 0x98, 0x3a, 0x9f, 0xde, 0xbc, 0xd9,
#};
]


#static const uint8_t kof2000_address_8_15_xor2[256] =
#{
kof2000_address_8_15_xor2 = [
	0x00, 0xbe, 0x06, 0x5a, 0xfa, 0x42, 0x15, 0xf2, 0x3f, 0x0a, 0x84, 0x93, 0x4e, 0x78, 0x3b, 0x89,
	0x32, 0x98, 0xa2, 0x87, 0x73, 0xdd, 0x26, 0xe5, 0x05, 0x71, 0x08, 0x6e, 0x9b, 0xe0, 0xdf, 0x9e,
	0xfc, 0x83, 0x81, 0xef, 0xb2, 0xc0, 0xc3, 0xbf, 0xa7, 0x6d, 0x1b, 0x95, 0xed, 0xb9, 0x3e, 0x13,
	0xb0, 0x47, 0x9c, 0x7a, 0x24, 0x41, 0x68, 0xd0, 0x36, 0x0b, 0xb5, 0xc2, 0x67, 0xf7, 0x54, 0x92,
	0x1e, 0x44, 0x86, 0x2b, 0x94, 0xcc, 0xba, 0x23, 0x0d, 0xca, 0x6b, 0x4c, 0x2a, 0x9a, 0x2d, 0x8b,
	0xe3, 0x52, 0x29, 0xf0, 0x21, 0xbd, 0xbb, 0x1f, 0xa3, 0xab, 0xf8, 0x46, 0xb7, 0x45, 0x82, 0x5e,
	0xdb, 0x07, 0x5d, 0xe9, 0x9d, 0x1a, 0x48, 0xce, 0x91, 0x12, 0xd4, 0xee, 0xa9, 0x39, 0xf1, 0x18,
	0x2c, 0x22, 0x8a, 0x7e, 0x34, 0x4a, 0x8c, 0xc1, 0x14, 0xf3, 0x20, 0x35, 0xd9, 0x96, 0x33, 0x77,
	0x9f, 0x76, 0x7c, 0x90, 0xc6, 0xd5, 0xa1, 0x5b, 0xac, 0x75, 0xc7, 0x0c, 0xb3, 0x17, 0xd6, 0x99,
	0x56, 0xa6, 0x3d, 0x1d, 0xb1, 0x2e, 0xd8, 0xbc, 0x2f, 0xde, 0x60, 0x55, 0x6c, 0x40, 0xcd, 0x43,
	0xff, 0xad, 0x38, 0x79, 0x51, 0xc8, 0x0e, 0x5f, 0xc4, 0x66, 0xcb, 0xa8, 0x7d, 0xa4, 0x3a, 0xea,
	0x27, 0x7b, 0x70, 0x8e, 0x5c, 0x19, 0x0f, 0x80, 0x6f, 0x8f, 0x10, 0xf9, 0x49, 0x85, 0x69, 0x7f,
	0xeb, 0x1c, 0x01, 0x65, 0x37, 0xa5, 0x28, 0xe4, 0x6a, 0x03, 0x04, 0xd1, 0x31, 0x11, 0x30, 0xfb,
	0x88, 0x97, 0xd3, 0xf6, 0xc5, 0x4d, 0xf5, 0x3c, 0xe8, 0x61, 0xdc, 0xd2, 0xb4, 0xb8, 0xa0, 0xae,
	0x16, 0x25, 0x02, 0x09, 0xfe, 0xcf, 0x53, 0x63, 0xaf, 0x59, 0xf4, 0xe1, 0xec, 0xd7, 0xe7, 0x50,
	0xe2, 0xc9, 0xaa, 0x4b, 0x8d, 0x4f, 0xe6, 0x64, 0xda, 0x74, 0xb6, 0x72, 0x57, 0x62, 0xfd, 0x58,
#};
]

#static const uint8_t kof2000_address_16_23_xor1[256] =
#{
kof2000_address_16_23_xor1 = [
	0x45, 0x9f, 0x6e, 0x2f, 0x28, 0xbc, 0x5e, 0x6d, 0xda, 0xb5, 0x0d, 0xb8, 0xc0, 0x8e, 0xa2, 0x32,
	0xee, 0xcd, 0x8d, 0x48, 0x8c, 0x27, 0x14, 0xeb, 0x65, 0xd7, 0xf2, 0x93, 0x99, 0x90, 0x91, 0xfc,
	0x5f, 0xcb, 0xfa, 0x75, 0x3f, 0x26, 0xde, 0x72, 0x33, 0x39, 0xc7, 0x1f, 0x88, 0x79, 0x73, 0xab,
	0x4e, 0x36, 0x5d, 0x44, 0xd2, 0x41, 0xa0, 0x7e, 0xa7, 0x8b, 0xa6, 0xbf, 0x03, 0xd8, 0x86, 0xdc,
	0x2c, 0xaa, 0x70, 0x3d, 0x46, 0x07, 0x80, 0x58, 0x0b, 0x2b, 0xe2, 0xf0, 0xb1, 0xfe, 0x42, 0xf3,
	0xe9, 0xa3, 0x85, 0x78, 0xc3, 0xd0, 0x5a, 0xdb, 0x1a, 0xfb, 0x9d, 0x8a, 0xa5, 0x12, 0x0e, 0x54,
	0x8f, 0xc5, 0x6c, 0xae, 0x25, 0x5b, 0x4b, 0x17, 0x02, 0x9c, 0x4a, 0x24, 0x40, 0xe5, 0x9e, 0x22,
	0xc6, 0x49, 0x62, 0xb6, 0x6b, 0xbb, 0xa8, 0xcc, 0xe8, 0x81, 0x50, 0x47, 0xc8, 0xbe, 0x5c, 0xa4,
	0xd6, 0x94, 0x4f, 0x7b, 0x9a, 0xcf, 0xe4, 0x59, 0x7a, 0xa1, 0xea, 0x31, 0x37, 0x13, 0x2d, 0xaf,
	0x21, 0x69, 0x19, 0x1d, 0x6f, 0x16, 0x98, 0x1e, 0x08, 0xe3, 0xb2, 0x4d, 0x9b, 0x7f, 0xa9, 0x77,
	0xed, 0xbd, 0xd4, 0xd9, 0x34, 0xd3, 0xca, 0x09, 0x18, 0x60, 0xc9, 0x6a, 0x01, 0xf4, 0xf6, 0x64,
	0xb4, 0x3a, 0x15, 0xac, 0x89, 0x52, 0x68, 0x71, 0xe7, 0x82, 0xc1, 0x0c, 0x92, 0xf7, 0x30, 0xe6,
	0x1c, 0x3e, 0x0f, 0x0a, 0x67, 0x35, 0xba, 0x61, 0xdd, 0x29, 0xc2, 0xf8, 0x97, 0x95, 0xb7, 0x3b,
	0xe0, 0xce, 0xf9, 0xd5, 0x06, 0x76, 0xb3, 0x05, 0x4c, 0x04, 0x84, 0x3c, 0x87, 0x23, 0x63, 0x7c,
	0x53, 0x56, 0xe1, 0x7d, 0x96, 0x1b, 0xd1, 0xec, 0x2a, 0x66, 0xf1, 0x11, 0x10, 0xff, 0x43, 0x2e,
	0xdf, 0x83, 0x74, 0xf5, 0x38, 0x20, 0xfd, 0xad, 0xc4, 0xb9, 0x55, 0x51, 0xb0, 0xef, 0x00, 0x57,
#};
]


#static const uint8_t kof2000_address_16_23_xor2[256] =
#{
kof2000_address_16_23_xor2 = [
	0x00, 0xb8, 0xf0, 0x34, 0xca, 0x21, 0x3c, 0xf9, 0x01, 0x8e, 0x75, 0x70, 0xec, 0x13, 0x27, 0x96,
	0xf4, 0x5b, 0x88, 0x1f, 0xeb, 0x4a, 0x7d, 0x9d, 0xbe, 0x02, 0x14, 0xaf, 0xa2, 0x06, 0xc6, 0xdb,
	0x35, 0x6b, 0x74, 0x45, 0x7b, 0x29, 0xd2, 0xfe, 0xb6, 0x15, 0xd0, 0x8a, 0xa9, 0x2d, 0x19, 0xf6,
	0x5e, 0x5a, 0x90, 0xe9, 0x11, 0x33, 0xc2, 0x47, 0x37, 0x4c, 0x4f, 0x59, 0xc3, 0x04, 0x57, 0x1d,
	0xf2, 0x63, 0x6d, 0x6e, 0x31, 0x95, 0xcb, 0x3e, 0x67, 0xb2, 0xe3, 0x98, 0xed, 0x8d, 0xe6, 0xfb,
	0xf8, 0xba, 0x5d, 0xd4, 0x2a, 0xf5, 0x3b, 0x82, 0x05, 0x16, 0x44, 0xef, 0x4d, 0xe7, 0x93, 0xda,
	0x9f, 0xbb, 0x61, 0xc9, 0x53, 0xbd, 0x76, 0x78, 0x52, 0x36, 0x0c, 0x66, 0xc1, 0x10, 0xdd, 0x7a,
	0x84, 0x69, 0xcd, 0xfd, 0x58, 0x0d, 0x6c, 0x89, 0x68, 0xad, 0x3a, 0xb0, 0x4b, 0x46, 0xc5, 0x03,
	0xb4, 0xf7, 0x30, 0x8c, 0x4e, 0x60, 0x73, 0xa1, 0x8b, 0xb1, 0x62, 0xcc, 0xd1, 0x08, 0xfc, 0x77,
	0x7e, 0xcf, 0x56, 0x51, 0x07, 0xa6, 0x80, 0x92, 0xdc, 0x0b, 0xa4, 0xc7, 0xe8, 0xe1, 0xb5, 0x71,
	0xea, 0xb3, 0x2f, 0x94, 0x18, 0xe2, 0x3d, 0x49, 0x65, 0xaa, 0xf1, 0x91, 0xc8, 0x99, 0x55, 0x79,
	0x86, 0xa7, 0x26, 0xa0, 0xac, 0x5f, 0xce, 0x6a, 0x5c, 0xf3, 0x87, 0x8f, 0x12, 0x1c, 0xd8, 0xe4,
	0x9b, 0x64, 0x2e, 0x1e, 0xd7, 0xc0, 0x17, 0xbc, 0xa3, 0xa8, 0x9a, 0x0e, 0x25, 0x40, 0x41, 0x50,
	0xb9, 0xbf, 0x28, 0xdf, 0x32, 0x54, 0x9e, 0x48, 0xd5, 0x2b, 0x42, 0xfa, 0x9c, 0x7f, 0xd3, 0x85,
	0x43, 0xde, 0x81, 0x0f, 0x24, 0xc4, 0x38, 0xae, 0x83, 0x1b, 0x6f, 0x7c, 0xe5, 0xff, 0x1a, 0xd9,
	0x3f, 0xb7, 0x22, 0x97, 0x09, 0xe0, 0xa5, 0x20, 0x23, 0x2c, 0x72, 0xd6, 0x39, 0xab, 0x0a, 0xee,
#};
]


#static const uint8_t kof2000_address_0_7_xor[256] =
#{
kof2000_address_0_7_xor = [
	0x26, 0x48, 0x06, 0x9b, 0x21, 0xa9, 0x1b, 0x76, 0xc9, 0xf8, 0xb4, 0x67, 0xe4, 0xff, 0x99, 0xf7,
	0x15, 0x9e, 0x62, 0x00, 0x72, 0x4d, 0xa0, 0x4f, 0x02, 0xf1, 0xea, 0xef, 0x0b, 0xf3, 0xeb, 0xa6,
	0x93, 0x78, 0x6f, 0x7c, 0xda, 0xd4, 0x7b, 0x05, 0xe9, 0xc6, 0xd6, 0xdb, 0x50, 0xce, 0xd2, 0x01,
	0xb5, 0xe8, 0xe0, 0x2a, 0x08, 0x1a, 0xb8, 0xe3, 0xf9, 0xb1, 0xf4, 0x8b, 0x39, 0x2d, 0x85, 0x9c,
	0x55, 0x73, 0x63, 0x40, 0x38, 0x96, 0xdc, 0xa3, 0xa2, 0xa1, 0x25, 0x66, 0x6d, 0x56, 0x8e, 0x10,
	0x0f, 0x31, 0x1c, 0xf5, 0x28, 0x77, 0x0a, 0xd1, 0x75, 0x34, 0xa4, 0xfe, 0x7d, 0x07, 0x51, 0x79,
	0x41, 0x90, 0x22, 0x35, 0x12, 0xbb, 0xc4, 0xca, 0xb2, 0x1f, 0xcb, 0xc8, 0xac, 0xdd, 0xd0, 0x0d,
	0xfc, 0xc5, 0x9d, 0x14, 0xbc, 0x83, 0xd9, 0x58, 0xc2, 0x30, 0x9a, 0x6a, 0xc0, 0x0c, 0xad, 0xf6,
	0x5d, 0x74, 0x7f, 0x2f, 0xbd, 0x1d, 0x47, 0xd5, 0xe6, 0x89, 0xcf, 0xb7, 0xd3, 0x59, 0x36, 0x98,
	0xf0, 0xfb, 0x3c, 0xf2, 0x3f, 0xa7, 0x18, 0x82, 0x42, 0x5c, 0xab, 0xba, 0xde, 0x52, 0x09, 0x91,
	0xaa, 0x61, 0xec, 0xd7, 0x95, 0x23, 0xcd, 0x80, 0xa5, 0x68, 0x60, 0x27, 0x71, 0xe1, 0x2c, 0x2e,
	0x8d, 0x2b, 0x57, 0x65, 0xbf, 0xc1, 0x19, 0xc7, 0x49, 0x64, 0x88, 0x4a, 0xcc, 0x20, 0x4e, 0xd8,
	0x3b, 0x4c, 0x13, 0x5f, 0x9f, 0xbe, 0x5e, 0x6e, 0xfd, 0xe2, 0xfa, 0x54, 0x37, 0x0e, 0x16, 0x7a,
	0x6c, 0x33, 0xb3, 0x70, 0x84, 0x7e, 0xc3, 0x04, 0xb0, 0xae, 0xb9, 0x81, 0x03, 0x29, 0xdf, 0x46,
	0xe5, 0x69, 0xe7, 0x24, 0x92, 0x5a, 0x4b, 0x5b, 0x94, 0x11, 0x3a, 0x3d, 0x87, 0xed, 0x97, 0xb6,
	0x32, 0x3e, 0x45, 0xaf, 0x1e, 0x43, 0x44, 0x8c, 0x53, 0x86, 0x6b, 0xee, 0xa8, 0x8a, 0x8f, 0x17,
#};
]











# void cmc_prot_device::decrypt(uint8_t *r0, uint8_t *r1,
					#uint8_t c0,  uint8_t c1,
					#const uint8_t *table0hi,
					#const uint8_t *table0lo,
					#const uint8_t *table1,
					#int base,
					#int invert)
                    #{
def change_data_block(c0, c1, table0hi, table0lo, table1, base, invert, address_0_7_xor, encrypt):
	#uint8_t tmp, xor0, xor1;

	#tmp = table1[(base & 0xff) ^ address_0_7_xor[(base >> 8) & 0xff]];
    tmp = table1[(base & 0xff) ^ address_0_7_xor[(base >> 8) & 0xff]]

	#xor0 = (table0hi[(base >> 8) & 0xff] & 0xfe) | (tmp & 0x01);
    xor0 = (table0hi[(base >> 8) & 0xff] & 0xfe) | (tmp & 0x01)

	#xor1 = (tmp & 0xfe) | (table0lo[(base >> 8) & 0xff] & 0x01);
    xor1 = (tmp & 0xfe) | (table0lo[(base >> 8) & 0xff] & 0x01)

	#if (invert)
	#{
    if invert:
		#*r0 = c1 ^ xor0;
		#*r1 = c0 ^ xor1;
        if encrypt: #???? not sure why this works
            return (c1 ^ xor1, c0 ^ xor0)
        else:
            return (c1 ^ xor0, c0 ^ xor1)
        #}
    else:
	#{

		#*r0 = c0 ^ xor0;
		#*r1 = c1 ^ xor1;
        return (c0 ^ xor0, c1 ^ xor1)
    #}
#}




def gfx_change_data(rom, rom_size, type0_t03, type0_t12, type1_t03, type1_t12, address_16_23_xor2, address_0_7_xor, encrypt):
    buf = bytearray(rom_size)
    for rpos in range(0, int(rom_size/4)):

        buf[4*rpos+0], buf[4*rpos+3] = change_data_block(rom[4*rpos+0], rom[4*rpos+3], type0_t03, type0_t12, type1_t03, rpos, (rpos>>8) & 1, address_0_7_xor, encrypt)
        
        # CHANGE FROM ORIGINAL ALGORITHM!!!
        # REVERSING THE TWO INPUT BYTES TO TEST. THE UNENCRYPTED WII ROM MIGHT BE STRIPED DIFFERENTLY.
        if encrypt:
            buf[4*rpos+1], buf[4*rpos+2] = change_data_block(rom[4*rpos+2], rom[4*rpos+1], type0_t12, type0_t03, type1_t12, rpos, ((rpos>>16) ^ address_16_23_xor2[(rpos>>8) & 0xff]) & 1, address_0_7_xor, encrypt)
        else:
            buf[4*rpos+2], buf[4*rpos+1] = change_data_block(rom[4*rpos+1], rom[4*rpos+2], type0_t12, type0_t03, type1_t12, rpos, ((rpos>>16) ^ address_16_23_xor2[(rpos>>8) & 0xff]) & 1, address_0_7_xor, encrypt)

    return buf

def gfx_change_address(input, rom_size, extra_xor, address_16_23_xor1, address_16_23_xor2, address_8_15_xor1, address_8_15_xor2, address_0_7_xor, encrypt):
    output = bytearray(rom_size)
    #referred_to = bytearray(rom_size)
    for rpos in range(0, int(rom_size/4)):
        baser = rpos

        baser ^= extra_xor # 0x31

        baser ^= address_8_15_xor1[(baser >> 16) & 0xff] << 8
        baser ^= address_8_15_xor2[baser & 0xff] << 8
        baser ^= address_16_23_xor1[baser & 0xff] << 16
        baser ^= address_16_23_xor2[(baser >> 8) & 0xff] << 16
        baser ^= address_0_7_xor[(baser >> 8) & 0xff]


        if (rom_size == 0x3000000): 
            if (rpos < int(0x2000000/4)):
                baser &= int(0x2000000/4)-1
            else:
                baser = int(0x2000000/4) + (baser & (int(0x1000000/4)-1))
        elif (rom_size == 0x6000000):
            if (rpos < int(0x4000000/4)):
                baser &= int(0x4000000/4)-1
            else:
                baser = int(0x4000000/4) + (baser & (int(0x1000000/4)-1))
        else: #/* Clamp to the real rom size */
            baser &= int(rom_size/4)-1

        # note: multiple "CPU-side" addresses point to same "ROM-side" addresses, meaning when decrypting, multiple output will duplicate the same input, and when encrypting, some output will just be nulls
        if encrypt:
            #output = the ROM address, input = the address the CPU sees.
            output[4*baser+0] = input[4*rpos+0]
            output[4*baser+1] = input[4*rpos+1]
            output[4*baser+2] = input[4*rpos+2]
            output[4*baser+3] = input[4*rpos+3]
        else:
            #output = the address the CPU sees, input = the ROM addresses
            output[4*rpos+0] = input[4*baser+0]
            output[4*rpos+1] = input[4*baser+1]
            output[4*rpos+2] = input[4*baser+2]
            output[4*rpos+3] = input[4*baser+3]
    return output








def encrypt_cmc50_gfx(unencrypted_crom, game_specific_xor_seed):
    print("Encrypting graphics with original CMC50 encryption...")
    encrypted_addresses = gfx_change_address(unencrypted_crom, len(unencrypted_crom), game_specific_xor_seed, kof2000_address_16_23_xor1, kof2000_address_16_23_xor2, kof2000_address_8_15_xor1, kof2000_address_8_15_xor2, kof2000_address_0_7_xor, True)
    return gfx_change_data(encrypted_addresses, len(unencrypted_crom), kof2000_type0_t03, kof2000_type0_t12, kof2000_type1_t03, kof2000_type1_t12, kof2000_address_16_23_xor2, kof2000_address_0_7_xor, True)

def decrypt_cmc50_gfx(encrypted_crom, game_specific_xor_seed):
    print("Decrypting graphics with CMC50 encryption...")
    unencrypted_data = gfx_change_data(encrypted_crom, len(encrypted_crom), kof2000_type0_t03, kof2000_type0_t12, kof2000_type1_t03, kof2000_type1_t12, kof2000_address_16_23_xor2, kof2000_address_0_7_xor, False)
    return gfx_change_address(unencrypted_data, len(encrypted_crom), game_specific_xor_seed, kof2000_address_16_23_xor1, kof2000_address_16_23_xor2, kof2000_address_8_15_xor1, kof2000_address_8_15_xor2, kof2000_address_0_7_xor, False)
