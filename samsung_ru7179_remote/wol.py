# def send_wol(mac_address):
#     """
#     Send the WOL "magic" packet to power a TV on.
#     :param mac_address: MAC address of the TV
#     :type mac_address: `str`
#     :return: `None`
#     :rtype: `None`
#     """
#     split_mac = mac_address.split(':')
#     hex_mac = list(int(h, 16) for h in split_mac)
#     hex_mac = struct.pack('BBBBBB', *hex_mac)
#
#     # create the magic packet from MAC address
#     packet = b'\xff' * 6 + (hex_mac * 16)
#
#     for ip in adapter_addresses.get_adapter_ips():
#         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#         sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         logger.debug('WOL: ' + repr(packet))
#         try:
#             sock.bind((ip, 0))
#             for _ in range(5):
#                 sock.sendto(packet, ('255.255.255.255', 9))
#                 sock.sendto(packet, ('255.255.255.255', 7))
#                 sock.sendto(packet, ('255.255.255.255', 0))
#         except socket.error:
#             pass
#
#         sock.close()
