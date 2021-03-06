import rpyc
# import socket
# from rpyc.utils.server import ThreadedServer
import configparser
import os
import math
import uuid
import random

# Main server service
class MainServerService(rpyc.Service):
    # expose main service to client
    class exposed_MainServer:
        block_size = 10             # size of each block
        replication_factor = 2     # number of replicates of each block
        subserver = []             # unique id for each subserver
        file_table = {}            # {target: [(block_id1, [sub-server1,...]),
                                   #           (block_id1, [sub-server1,...]),
                                   #           ......                       ]                 
                                   # }
        # block_table =                       [(block_id1, [sub-server1,...]),
                                   #           (block_id1, [sub-server1,...]),
                                   #           ......                       ] 


        # Return file table entry corresponding to <target>
        def exposed_get_file_table(self, target):
            if target in self.__class__.file_table:
                return self.__class__.file_table[target]
            return None
        
        def exposed_get_subserver_list(self):
            return self.__class__.subserver

        def exposed_get_sub_server(self, block_id):
            return [self.__class__.subserver[_] for _ in block_id]

        # Create file table entry (empty) for target file based on source file sizes
        # Return:
        #   block_table -> (block id, sub server id) tuple array
        def exposed_creat_file_table_entry(self, target, src_size):
            if target not in self.__class__.file_table:
                # Create entry for thix file 
                # self.__class__.file_table[target] = []
                self.__class__.file_table[target] = None
            # num_block = self.get_num_blocks(src_size)
            num_block = 1
            tpl = self.get_blocks_table(target, num_block)     
            return tpl

        # Return the number of block needed for storing file of size <size>
        def get_num_blocks(self, size):
            return int(math.ceil((float(size) / self.__class__.block_size)))

        def exposed_delete_file(self, target):
            del self.__class__.file_table[target]

        def exposed_rename_file(self, target, newname):
            self.__class__.file_table[newname] = self.__class__.file_table.pop(target)

        def exposed_get_block_size(self):
            return self.__class__.block_size

        # Assign a number of block with random sub servers
        # Return the block table(block id, subserver id) array of current target.
        def get_blocks_table(self, target, num_block):
            block_table = []
            for _ in range(num_block): # For now, just one
                # get id for each block
                block_id = uuid.uuid1()
                # get id for target sub server 
                #subserver_ids = random.sample(self.__class__.subserver, self.__class__.replication_factor)
                subserver_id = [random.choice(self.__class__.subserver)]
                # add (block id, sub server id) as a tuple in <blocks>
                tpl = (block_id, subserver_id)
                # add tuple to file table
                # Todo: What is target?
                block_table.append(tpl)
                self.__class__.file_table[target] = block_table
            return block_table

