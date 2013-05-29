#!/usr/bin/python2.7
__author__ = 'Kailai Shao'

import xml.dom.minidom
import os


def main():
    if os.path.exists('output') == False:
        os.mkdir('output')

    dom = xml.dom.minidom.parse('mpc5643l_irqs_db.xml')
    list = dom.getElementsByTagName('Irq')


    #Isr_Implement.h
    if os.path.exists("output/Isr_Implement.h"):
        os.remove("output/Isr_Implement.h")

    f = open("output/Isr_Implement.h", "w")
    f.write(generate_head('Isr_Implement.h'))
    f.write("""\
#ifndef ISR_IMPLEMENT_H
#define ISR_IMPLEMENT_H
#include "MPC5643L.h"

#include "Irq_Cfg.h"

""")

    for i in list:
        if i.childNodes[0].nodeValue.strip() == 'UnUsed':
            f.write('//#define ')
        else:
            f.write('  #define ')
        f.write(i.childNodes[0].nodeValue.strip())
        f.write('    ')
        f.write(i.attributes['id'].value)
        f.write('\n')

    f.write('\n\n')
    for i in list:
        irqName = i.childNodes[0].nodeValue.strip()
        if irqName != 'UnUsed':
            f.write('#if(IRQ_' + irqName + ' == STD_ON)\n')
            f.write('void ' + irqName + '_ISR(void);\n#endif\n\n')

    f.write('\n#endif')

    f.close()


    #Isr_Implement.c
    if os.path.exists("output/Isr_Implement.c"):
        os.remove("output/Isr_Implement.c")

    f = open("output/Isr_Implement.c", "w")

    f.write(generate_head('Isr_Implement.c'))
    f.write("""\
#include "MPC5643L.h"
#include "Isr_Implement.h"

#include "Irq_Cfg.h"

""")

    for i in list:
        irqName = i.childNodes[0].nodeValue.strip()
        if irqName != 'UnUsed':
            irqId = i.attributes['id'].value
            irqCategory = i.attributes['category'].value
            f.write(generate_isr(irqName, irqId, irqCategory))

    f.close()


    #Isr_Vector.h
    if os.path.exists("output/Isr_Vector.h"):
        os.remove("output/Isr_Vector.h")

    f = open("output/Isr_Vector.h", "w")

    f.write(generate_head('Isr_Vector.h'))
    f.write("""\
#ifndef ISR_VECTOR_H
#define ISR_VECTOR_H
#include "MPC5643L.h"

void INTCTblInit(void);

#endif
""")


    #Isr_Vector.c
    if os.path.exists("output/Isr_Vector.c"):
        os.remove("output/Isr_Vector.c")

    f = open("output/Isr_Vector.c", "w")

    f.write(generate_head('Isr_Vector.c'))
    f.write("""\
#include "MPC5643L.h"
#include "INTCInterrupts.h"
#include "Isr_Vector.h"
#include "Isr_Implement.h"

#include "Irq_Cfg.h"

""")

    f.write('void INTCTblInit(void)\n{\n')
    for i in list:
        irqName = i.childNodes[0].nodeValue.strip()
        if irqName != 'UnUsed':
            irqId = i.attributes['id'].value
            f.write(generate_vector(irqName, irqId))

    f.write('}\n')


    #Irq_Cfg.h
    if os.path.exists("output/Irq_Cfg.h"):
        os.remove("output/Irq_Cfg.h")

    f = open("output/Irq_Cfg.h", "w")

    f.write(generate_head('Irq_Cfg.h'))
    f.write("""\
#!Only For Test
#ifndef IRQ_CFG_H
#define IRQ_CFG_H

""")
    for i in list:
        irqName = i.childNodes[0].nodeValue.strip()
        if irqName != 'UnUsed':
            f.write('#define IRQ_' + irqName + '    STD_OFF\n')

    f.write('\n\n')
    for i in list:
        irqName = i.childNodes[0].nodeValue.strip()
        if irqName != 'UnUsed':
            f.write('#define NESTABLE_' + irqName + '_ISR    STD_OFF\n')

    f.write('\n\n')
    for i in list:
        irqName = i.childNodes[0].nodeValue.strip()
        if irqName != 'UnUsed':
            f.write('#define PRIO_' + irqName + '_ISR    4\n')

    f.write('\n#endif')

    f.close()


def generate_head(entity_filename):
    template = """\
/*
*********************************************************************************
* Copyright (c) 2013,Embedded System Engineering Center of Zhejiang University
* All rights reserved.
*
* FILE NAME: %(entity_filename)s
* DESCRIPTION:
* UPDATE HISTORY
* REV      AUTHOR        DATE         DESCRIPTION OF CHANGE
* 1.0      Kailai Shao   29/MAR/13    Initial version.
*
*********************************************************************************
*/


"""
    return template % locals()


def generate_isr(entity_name, entity_id, entity_category):
    template = """\
//------------------------------------------------------------------------------------
// Interrupt Service Routine for %(entity_name)s
// IRQ #%(entity_id)s
// Source module :%(entity_category)s
//------------------------------------------------------------------------------------
#if (IRQ_%(entity_name)s == STD_ON)
void %(entity_name)s_ISR(void)
{
#if(NESTABLE_%(entity_name)s_ISR == STD_ON)
    IntEnter_Nesting();
#else
    IntEnter_Unnesting();
#endif

    if(ISRVector[%(entity_name)s] != NULL)
    {
        ISRVector[%(entity_name)s]();
    }

    //Clear interrupt flag
    //TODO

    //Execute MCAL ISR
    //TODO

#if(NESTABLE_%(entity_name)s_ISR == STD_ON)
    IntExit_Nesting();
#else
    IntExit_Unnesting();
#endif
}
#endif


"""
    return template % locals()


def generate_vector(entity_name, entity_id):
    template = """\
#if (IRQ_%(entity_name)s == STD_ON)
    INTC_InstallINTCInterruptHandler(%(entity_name)s_ISR,%(entity_id)s,PRIO_%(entity_name)s_ISR);
#else
    INTC_InstallINTCInterruptHandler(NULL,%(entity_id)s,NULL);
#endif

"""
    return template % locals()


if __name__ == '__main__':
    main()