#!/usr/bin/env python3

import sys



FRAME       =   0
BUTTON      =   1
LABEL       =   2
COMMENT     =   3
PROPERTY    =   4
UNKNOWN     =   5
CONTROL     =   6

POSSIBLE_CONTROLS=["Label", "Frame", "Button"]

class TkControl(object):
    def __init__(self, line):
        l=line[:-1].strip()
        self.control_type=l
        self.properties=[]
        self.children=[]
        self.parent=None
        
    def set_parent(self, parent):
        self.parent=parent
        
    def add_property (self, line):
        line=line
        slices=line.split(":")
        key=slices[0].strip()
        value=slices[1].strip()
        self.properties.append ( (key, value))
        
    def add_child(self, node):
        self.children.append( node )
        
        
    def get_property_value(self, property_key):
        for tup in self.properties:
            (key, value) = (tup[0], tup[1])
            if key==property_key:
                return value
        return None
    
    def get_id(self):
        return self.get_property_value("id")
    
    def get_pack(self):
        pack_properties=[]
        fill_value=self.get_property_value("fill")
        if fill_value!=None:
            pack_properties.append("fill="+fill_value)
        expand_value=self.get_property_value("expand")
        if expand_value!=None:
            pack_properties.append("expand="+expand_value)
        
        return ",".join ( pack_properties )
            
    def generate_code(self):
        EOL="\n"
        code=""
        parent_id=self.parent
        code+="        "+self.get_id()+"="+self.control_type +"("+parent_id+")"+ EOL
        code+="        "+self.get_id()+".pack(" + self.get_pack()  + ")" + EOL
        
        for child in self.children:
            child.set_parent(self.get_id())
            code +=child.generate_code()
        return code
    
    def __str__(self):
        return self.control_type
        
        
def get_indentation_level(line, spaces=4):
    pos=0
    while line[pos]==' ':
        pos=pos+1
    return int(pos/spaces)

def extract_properties(line):
    stripped_line=line.strip()
    slices=line.split(":")
    (key, value) = (slices[0].strip, slices[1].strip)
    return  (key, value)


def is_comment(line):
    stripped_line=line.strip()
    if stripped_line[0]=='#':
        return True
    return False

def is_control(line):
    stripped_line=line.strip()
    line_without_colon=stripped_line[:-1]
    if line_without_colon in POSSIBLE_CONTROLS:
        return True
    return False

def is_property(line):
    stripped_line=line.strip()
    if stripped_line[-1]!=':':
        return True
    return False
    
def get_line_type(line):
    if is_comment(line):
        return COMMENT
    if is_property(line):
        return PROPERTY
    if is_control(line):
        return CONTROL
    return None
    
def parse(filename):
    #print ("Parsing "+filename+"...")
    lines=[]
    with open(filename, "r", encoding="utf-8") as fd:
        lines=fd.readlines()
    
    clear_lines=map(lambda x: x.rstrip(), lines)
    filtered_lines=filter(lambda x: x!="", clear_lines)
    current_indentation_level=0
    line_number=0
    for l in filtered_lines:
        line_number+=1
        ind_level=get_indentation_level(l)
        if ind_level==current_indentation_level+1:
            current_indentation_level+=1
        if ind_level>current_indentation_level+1:
            print ("Parse error, wrong indentation level")
            print ("Line "+str(line_number)+": "+l)
            return
    build_ui(lines)
    
  
def get_template_file():
    EOL="\n"
    text=""
    with open("template.py", "r") as fd:
        lines=fd.readlines()
        text ="".join ( lines )
    return text

    
def build_ui(lines):
    stack_level=0
    line_number=0
    stack=[]
    current_indentation_level=0
    clear_lines=map(lambda x: x.rstrip(), lines)
    filtered_lines=filter(lambda x: x!="", clear_lines)
    for l in filtered_lines:
        line_number+=1
        ind_level=get_indentation_level(l)
        line_type=get_line_type(l)
        
        
        #print ("\t"*ind_level, ind_level, current_indentation_level, line_type, l)
        
        if line_type==CONTROL and ind_level==0:
            #print("Pushing:"+l)
            current_node=TkControl(l)
            stack.append(current_node)
            continue
        

        if line_type==CONTROL and ind_level==current_indentation_level+1:
            current_indentation_level+=1
            last_node=stack[-1]
            new_node=TkControl(l)
            last_node.add_child(new_node)
            stack.append(new_node)
            #print("Pushing:"+l)
            continue
        
        if line_type==PROPERTY and ind_level==current_indentation_level+1:
            last_node=stack[-1]
            last_node.add_property(l)
            #print ("Property-->"+l+" for "+str(last_node))
            continue
        
        if line_type==CONTROL and ind_level==current_indentation_level:
            stack.pop()
            last_node=stack[-1]
            new_node=TkControl(l)
            last_node.add_child(new_node)
            stack.append(new_node)
            #print("Pushing:"+l)
            continue
        
        if line_type==CONTROL and ind_level<current_indentation_level:
            dif =current_indentation_level-ind_level
            current_indentation_level=ind_level
            for i in range(0, dif+1):
                #print("Unshifting in "+l+", "+str(dif))
                stack.pop()
            last_node=stack[-1]
            new_node=TkControl(l)
            last_node.add_child(new_node)
            stack.append(new_node)
            #print("Pushing:"+l)
            
            
    stack[0].set_parent("self.main_window")
    code=stack[0].generate_code()
    template=get_template_file()
    
    print (template.format(code))
if __name__ == '__main__':
    try:
        parse(sys.argv[1])
    except IndexError:
        print("Usage: pyyaml2tkinter <filename>")