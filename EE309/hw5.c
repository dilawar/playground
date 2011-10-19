#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#define False 0
#define True 1

void Usart_Init(void)
{
    UBRRH = 0x00;
    UBRRL = 0x33;
    UCSRB = (1<< RXEN)|(1<< TXEN);
    UCSRC = (1<<URSEL)|(1<< UCSZ1)|(1<< UCSZ2);
}

void USART_Transmit(unsigned int data)
{
    while(!(UCSRA & (1<<UDRE)))
    {}
    UDR = data;
}

void PORTs_init(void)
{
    DDRA = 0x0F;
    DDRD = (1<<PD5);
}

void PWM_init (unsigned int compare)
{
    TCCR1A = (1<< COM1A1)|(1<<WGM10);
    TCCR1B = (1<< CS10) | (1<< WGM12);
    OCR1AH = compare;
    OCR1AL = compare << 8;
}

int main()
{
    unsigned int keypress = 0;
    PORTs_init();
    Usart_Init();

    while(1)
    {
        int detected = False;
        PORTA = 0xFE;
        int a = PINA;
        a = a & 0xF0;
        if(a == 0xE0)
        {
            USART_Transmit(30);
            detected = True;
        }

        else if(a == 0xD0)
        {
            USART_Transmit(31);
            detected = True;
        }
        
        else if(a == 0xB0)
        {
            USART_Transmit(32);
            detected = True;
        }
        else if(a == 0x70)
        {
            USART_Transmit(33);
            detected = True;
        }
        
        /*  second time */
        PORTA = 0xFD;
         a = PINA;
        a = a & 0xF0;
        if(a == 0xE0 && (detected == False))
        {
            USART_Transmit(34);
            detected = True;
        }

        else if(a == 0xD0 && (detected == False))
        {
            USART_Transmit(35);
            detected = True;
        }
        
        else if(a == 0xB0 &&(detected == False))
        {
            USART_Transmit(36);
            detected = True;
        }
        else if(a == 0x70 && (detected == False))
        {
            USART_Transmit(37);
            detected = True;
        }
        
     /*  third  time */
        PORTA = 0xFB;
        a = PINA;
        a = a & 0xF0;
        if(a == 0xE0 && (detected == False))
        {
            USART_Transmit(38);
            detected = True;
        }

        else if(a == 0xD0 && (detected == False))
        {
            USART_Transmit(39);
            detected = True;
        }
        
        else if(a == 0xB0 &&(detected == False))
        {
            USART_Transmit(40);
            detected = True;
        }
        else if(a == 0x70 && (detected == False))
        {
            USART_Transmit(41);
            detected = True;
        }
     /*  last time */
        PORTA = 0xF7;
        a = PINA;
        a = a & 0xF0;
        if(a == 0xE0 && (detected == False))
        {
            USART_Transmit(42);
            detected = True;
        }

        else if(a == 0xD0 && (detected == False))
        {
            USART_Transmit(43);
            detected = True;
        }
        
        else if(a == 0xB0 &&(detected == False))
        {
            USART_Transmit(44);
            detected = True;
        }
        else if(a == 0x70 && (detected == False))
        {
            USART_Transmit(45);
            detected = True;
        }

        else 
            USART_Transmit(90);
    }
    return 0;
}







////        if (keypress == 0)
//        {
//            PORTA = PORTA & 0b11111101;
//
//            if((PORTA & 0b00010000) == 0x00)
//                keypress = 05;
//
//            else if((PORTA & 0b00100000) == 0x00)
//                keypress = 6;
//
//            else if((PORTA & 0b01000000) == 0x00)
//                keypress = 7;
//
//            else if((PORTA & 0b10000000) == 0x00)
//                keypress = 8;
//        } 
//
//
//        if (keypress == 0)
//        {
//            PORTA = PORTA & 0b11111011;
//
//            if((PORTA & 0b00010000) == 0x00)
//                keypress = 9;
//
//            else if((PORTA & 0b00100000) == 0x00)
//                keypress = 10;
//
//            else if((PORTA & 0b01000000) == 0x00)
//                keypress = 11;
//
//            else if((PORTA & 0b10000000) == 0x00)
//                keypress = 12;
//        }   
//
//
//        if (keypress == 0)
//        {
//            PORTA = PORTA & 0b11110111;
//
//            if((PORTA & 0b00010000) == 0x00)
//                keypress = 13;
//
//            else if((PORTA & 0b00100000) == 0x00)
//                keypress = 14;
//
//            else if((PORTA & 0b01000000) == 0x00)
//                keypress = 15;
//
//            else if((PORTA & 0b10000000) == 0x00)
//                keypress = 16;
//        } 
//
//        if(keypress!=0)
//        {
//            USART_Transmit(keypress+30);
//            PWM_init(keypress * 16);
//        }
//        else 
//        {
//            USART_Transmit(63);
//        }
//    }
//}
