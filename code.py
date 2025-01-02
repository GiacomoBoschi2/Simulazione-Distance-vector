'''
Boschi Giacomo, Matricola: 0001071364
Il seguente progetto per Reti di Telecomunicazioni mostra il funzionamento del protocollo di routign Distance Vector (DV)
'''

'''
Nota: lo scopo di questo progetto è mostrare la logica di Distance Vector.
Di conseguenza,i miglioramenti dati da OSPF, che risolvono alcuni dei problemi di DV non sono implementati
'''

#La seguente classe gestisce la logica relativa al singolo nodo di rete (router)
#Ogni router ha un suo identificativo,per semplificare il lavoro qualunque stringa è accettata e non deve essere necessariamente un indirizzo IP valido

class routing_node:
    def __init__(self, name):
        self.name = name
        self.route_table = {} #la routing table è un dictionary contenente la distanza dagli altri nodi (key = identificativo nodo, value = distanza)
        self.direct_links = {} #contiene le distanze dei collegamenti diretti coi nodi
        self.neighbors = [] #usato per leggere le routing table dei vicini
        self.next_hops = {} #il next hop per un dato nodo

        #distanza da se stesso
        self.route_table[self.name] = 0
        self.next_hops[self.name] = self.name

    #resetta la routing table lasciando soltanto i collegamenti diretti,cancella i next_hops
    def reset_routing_table(self):
        self.route_table = {}
        self.next_hops = {}

        for node in self.direct_links:
            self.route_table[node] = self.direct_links[node]

        #senza informazioni aggiuntive il next_hop
        for node in self.neighbors:
            self.next_hops[node.name] = node.name
        #distanza da se stesso
        self.route_table[self.name] = 0
        self.next_hops[self.name] = self.name

    #utilizza le routing table dei vicini per aggiornarsi
    def update_routing_table(self):
        for node in self.neighbors:
            for neighbor in node.route_table:
                '''aggiornamento con logica di bellman-ford: per ogni vicino del mio vicino diretto,guardo se ho una distanza migliore usando come next hop
                il mio diretto vicino, ed eventualmente aggiorno se necessario'''
                dist = self.route_table[node.name] + node.route_table[neighbor]
                #aggiorno se è la prima volta che mi imbatto nel nodo o la distanza è migliore
                if not (neighbor in self.route_table.keys()):
                    self.route_table[neighbor] = dist
                    self.next_hops[neighbor] = node.name
                elif self.route_table[neighbor] > dist:
                    self.route_table[neighbor] = dist
                    self.next_hops[neighbor] = node.name

    #stampa la propria routing table e next_hops
    def dump_content(self):
        print("Tabella di "+self.name)
        for key in self.route_table:
            if key != self.name:
                print("DESTINAZIONE:" + key + "    NEXT_HOP:"+self.next_hops[key]+"    DISTANZA:"+str(self.route_table[key]))

    #aggiunge un vicino al nodo
    def add_neighbor(self, node, dist):
        self.neighbors.append(node)
        self.route_table[node.name] = dist
        self.next_hops[node.name] = node.name
        self.direct_links[node.name] = dist

#gestisce i nodi di una rete e i suoi collegamenti
class network_manager:
    def __init__(self):
        self.nodes = {}
    def __init__ (self,nodes):
        self.nodes = nodes

    #aggiungi un nodo
    def add(self, node):
        self.nodes[node.name] = node

    #aggiungi collegamento tra due nodi
    def connect(self, node1, node2, dist):
        self.nodes[node1].add_neighbor(self.nodes[node2], dist)
        self.nodes[node2].add_neighbor(self.nodes[node1], dist)

    #esegui l'algoritmo DV sulla rete
    def run_DV(self):
        for node in self.nodes.values():
            node.reset_routing_table() #ogni routing table si resetta (questo per evitare i classici problemi di DV, che non sono gestiti in questo progetto)

        node_count = len(self.nodes.keys())
        for i in range(node_count):
            #singolo round di bellman-ford
            for node in self.nodes.values():
                node.update_routing_table()

    #stampa completa delle routing table di ogni nodo
    def dump_tables(self):
        for node in self.nodes.values():
            node.dump_content()
            print()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    example_manager = network_manager({})

    #la rete di esempio è quella nell'immagine, una rete di 7 router
    for i in range(1,8):
        example_manager.add(routing_node("router n."+str(i)))

    #collegamenti
    example_manager.connect("router n.1", "router n.2", 5)
    example_manager.connect("router n.1", "router n.3", 3)
    example_manager.connect("router n.1", "router n.4", 4)
    example_manager.connect("router n.2", "router n.3", 2)
    example_manager.connect("router n.3", "router n.7", 2)
    example_manager.connect("router n.3", "router n.5", 2)
    example_manager.connect("router n.4", "router n.6", 7)
    example_manager.connect("router n.5", "router n.6", 1)

    #run
    example_manager.run_DV()
    example_manager.dump_tables()