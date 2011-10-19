#include<avr/io.h>
#include<util/delay.h>

void USART_init(unsigned int baud)
{
	UBRRH=(unsigned char)(baud>>8);
	UBRRL=(unsigned char)(baud);
	UCSRB=_BV(TXEN)|_BV(RXEN);
	UCSRC=(_BV(URSEL)|_BV(UCSZ1)|_BV(UCSZ0));
}

void USART_transmit(unsigned char data)
{
	while(!(UCSRA & _BV(UDRE)));
	UDR=data;
}

void PORT_init(void)
{
	DDRA=0xF0;
	PORTA=0x0F;
	DDRD=_BV(PD5);
}

void PWM_init(void)
{
	TCCR1A=_BV(WGM10)|_BV(COM1A1);
	TCCR1B=_BV(WGM12)|_BV(CS11);
	OCR1A=0;
}

int main()
{
	USART_init(51);
	PORT_init();
	PWM_init();
	unsigned char keypress='0';
	int a;
	while(1)
	{
		a=PINA;
		a=a&0x0F;
		if(a!=0x0F)
		{
			PORTA=0xEF;
			//_delay_ms(1.0);
			a=PINA;
			a=a&0x0F;
			if(a==0x0E)
			{
				keypress='a';
				OCR1AL=0x30;
			}
			else if(a==0x0D)
			{
				keypress='b';
				OCR1AL=0x20;
			}
			else if(a==0x0B)
			{
				keypress='c';
				OCR1AL=0x10;
			}
			else if(a==0x07)
			{
				keypress='d';
				OCR1AL=0x00;
			}
			PORTA=0xDF;
			//_delay_ms(1.0);
			a=PINA;
			a=a&0x0F;
			if(a==0x0E)
			{
				keypress='e';
				OCR1AL=0x70;
			}
			else if(a==0x0D)
			{
				keypress='f';
				OCR1AL=0x60;
			}
			else if(a==0x0B)
			{
				keypress='g';
				OCR1AL=0x50;
			}
			else if(a==0x07)
			{
				keypress='h';
				OCR1AL=0x40;
			}
			PORTA=0xBF;
			//_delay_ms(1.0);
			a=PINA;
			a=a&0x0F;
			if(a==0x0E)
			{
				keypress='i';
				OCR1AL=0xB0;
			}
			else if(a==0x0D)
			{
				keypress='j';
				OCR1AL=0xA0;
			}
			else if(a==0x0B)
			{
				keypress='k';
				OCR1AL=0x90;
			}
			else if(a==0x07)
			{
				keypress='l';
				OCR1AL=0x80;
			}
			PORTA=0x7F;
			//_delay_ms(1.0);
			a=PINA;
			a=a&0x0F;
			if(a==0x0E)
			{
				keypress='m';
				OCR1AL=0xF0;
			}
			else if(a==0x0D)
			{
				keypress='n';
				OCR1AL=0xE0;
			}
			else if(a==0x0B)
			{
				keypress='o';
				OCR1AL=0xD0;
			}
			else if(a==0x07)
			{
				keypress='p';
				OCR1AL=0xC0;
			}
			PORTA=0x0F;
			//_delay_ms(1.0);
			USART_transmit(keypress);
		}
		else
		{
			USART_transmit('z');
		}
	}
	//_delay_ms(100.0);
	return 0;
}
