# include <avr/io.h>
# include <util/delay.h>
# include <avr/interrupt.h>

void USART_Init(unsigned int baud)
{

    UBRRH = 0; //set baud value
    UBRRL = 51; 
    UCSRB = 24; //Enable transmitter and reciever
    UCSRC = 134;

}

void USART_Transmit( char data )
{

    while ( !( UCSRA & (1<<UDRE)) );


    UDR = data;
}

void PORTs_init(void)
{
    DDRA=0xF0;
    PORTA=0x0F;
    DDRD=(1<<PD5);
}


int main()
{
    char keypress='A';
    USART_Init(51);
    PORTs_init();
    unsigned int a = 0;
    while(1)
    {
        a=PINA;
        a=a&0x0F;
        if(a!=0x0F)
        {
            USART_Transmit('*');
            PORTA=0xEF;
            a=PINA;
            a=a&0x0F;
            if(a==0x0E)      {USART_Transmit('a'); keypress='4';}
            else if(a==0x0D) {USART_Transmit('b'); keypress='8';}
            else if(a==0x0B) {USART_Transmit('c'); keypress='C';}
            else if(a==0x07) {USART_Transmit('d'); keypress='0';}
            else
            {
                USART_Transmit('/');
				PORTA=0xDF;
                a=PINA;
                a=a&0x0F;
                if(a==0x0E)      {USART_Transmit('e');keypress='3';}
                else if(a==0x0D) {USART_Transmit('f');keypress='7';}
                else if(a==0x0B) {USART_Transmit('g');keypress='B';}
                else if(a==0x07) {USART_Transmit('h');keypress='F';}
                else
               {
			   		USART_Transmit('+');
                    PORTA=0xBF;
                    a=PINA;
                    a=a&0x0F;
                    if(a==0x0E)      {USART_Transmit('i');keypress='2';}
                    else if(a==0x0D) {USART_Transmit('j');keypress='6';}
                    else if(a==0x0B) {USART_Transmit('k');keypress='A';}
                    else if(a==0x07) {USART_Transmit('l');keypress='E';}
                    else
                    {
					    USART_Transmit('-');
                        PORTA=0x7F;
                        a=PINA;
                        a=a&0x0F;
                        if(a==0x0E)      {USART_Transmit('m');keypress='1';}
                        else if(a==0x0D) {USART_Transmit('n');keypress='5';}
                        else if(a==0x0B) {USART_Transmit('o');keypress='9';}
                        else if(a==0x07) {USART_Transmit('p');keypress='D';}
                        else 
                            { USART_Transmit('%');}

                    }

                }

            }
            USART_Transmit(keypress);
            PORTA=0x0F;
        }
    }
}
