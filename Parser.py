from Point import Point


class Parser:
    @staticmethod
    def parseAllVertex(path):
        with open(path, 'r') as f:
            text = f.read().split('\n')
            vertexList = [row for row in text if row.startswith('v ')]
            vertexListVN = [row for row in text if row.startswith('vn ')]
            coordList, coordListVN = [], []
            for vertex in vertexList:
                coord = vertex.split(' ')
                coordList.append(Point(float(coord[1]), float(coord[2]), float(coord[3])))
            for vertex in vertexListVN:
                coord = vertex.split(' ')
                coordListVN.append(Point(float(coord[1]), float(coord[2]), float(coord[3])))
            return coordList, coordListVN

    @staticmethod
    def parseAllPolygon(path):
        with open(path, 'r') as f:
            text = f.read().split('\n')
            polygonList = [row for row in text if row.startswith('f ')]
            resultList, normalList = [], []
            for polRow in polygonList:
                vertexIndexes = polRow.split(' ')
                vertexIndex1 = vertexIndexes[1].split("/")[0]
                vertexIndex2 = vertexIndexes[2].split("/")[0]
                vertexIndex3 = vertexIndexes[3].split("/")[0]

                if len(vertexIndexes[1].split("/")) == 3:
                    normalIndex1 = vertexIndexes[1].split("/")[2]
                    normalIndex2 = vertexIndexes[2].split("/")[2]
                    normalIndex3 = vertexIndexes[3].split("/")[2]
                    normalList.append([int(normalIndex1), int(normalIndex2), int(normalIndex3)])

                resultList.append([int(vertexIndex1), int(vertexIndex2), int(vertexIndex3)])

            return resultList, normalList
