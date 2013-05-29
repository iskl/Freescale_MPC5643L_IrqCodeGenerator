__author__ = 'Kailai Shao'
import xml.dom.minidom
import codecs

impl = xml.dom.minidom.getDOMImplementation()
dom = impl.createDocument(None, 'MPC5643L', None)
root = dom.documentElement
root.setAttribute('author', 'Kailai Shao')
root.setAttribute('date', '2013.5.29')

f = open("irqs.txt")
irqsLines = f.readlines()
f.close()

index = 0
category = ""
for i in range(0, len(irqsLines)):
    line = irqsLines[i]
    if line[0] == '#':
        category = line[1:len(line) - 1]
    elif line[0] == '~':
        item = dom.createElement('Irq')
        item.setAttribute('id', str(index))
        item.setAttribute('category', 'UnUsed')
        index += 1
        text = dom.createTextNode('UnUsed')
        item.appendChild(text)
        root.appendChild(item)
    else:
        item = dom.createElement('Irq')
        item.setAttribute('id', str(index))
        item.setAttribute('category', category)
        index += 1
        text = dom.createTextNode(category + "_" + line[0:len(line) - 1])
        item.appendChild(text)
        root.appendChild(item)
        #print root.toprettyxml()

print root.toprettyxml()
f = file("mpc5643l_irqs_db.xml", "w")
writer = codecs.lookup('utf-8')[3](f)
dom.writexml(writer, encoding='utf-8', newl='\n', addindent='    ')
writer.close()

