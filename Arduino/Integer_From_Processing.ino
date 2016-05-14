// BinaryDataFromProcessing
// These defines must mirror the sending program:

#define     DELAY    10
const char HEADER       = 'H';
const char A_TAG    = 'M';
const char B_TAG    = 'X';
const int  TOTAL_BYTES  = 10  ; // the total bytes in a message

const int fill_size_ = 48;
int fill_[ fill_size_ ];

int incoming = 0;
int totalRead = 0;

void setup()
{
    Serial.begin(9600);
    pinMode(6,INPUT);
    for( size_t i = 0; i < fill_size_; i++ )
        fill_[i] = 0;
}

void print_fill( void )
{
    for (size_t i = 0; i < fill_size_; i++) 
    {
        Serial.print( fill_[i] );
        Serial.print( " " );
    }
    Serial.print("\n");
}

void loop()
{
    if ( Serial.available() > 0 )
    {
        fill_[ totalRead % fill_size_] = Serial.read();
        totalRead += 1;
        delay( DELAY );
        Serial.println( incoming );
    }
    print_fill( );


#if 0
        if( Serial.read() == HEADER)
        {
            char tag = Serial.read();
            if(tag == A_TAG)
            {
                Serial.println( "Reading " + Serial.read() );
                //Collect integers
                int a = Serial.read() * 256; 
                a = a + Serial.read();
                int b = Serial.read() * 256;
                b = b + Serial.read();
                int c = Serial.read() * 256;
                c = c + Serial.read();
                int d = Serial.read() * 256;
                d = d + Serial.read();

                Fill[0]=a;
                Fill[1]=b;
                Fill[2]=c;
                Fill[3]=d;

                Serial.print("Received integers | a:");
                Serial.print(a);
                Serial.print(", b:");
                Serial.println(b);
                Serial.print(", c:");
                Serial.println(c);
                Serial.print(", d:");
                Serial.println(d);
            }
            else {
                Serial.print("got message with unknown tag ");
                Serial.write(tag);
            }
        }
    }

    if (digitalRead(6)==HIGH){
        for (int i=0; i<4; i++){
            Serial.println(Fill[i]);
        }
        delay(2000);
    } 
#endif

}
