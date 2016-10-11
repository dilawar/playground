import cv2
import time

properties = { 'fps' : (cv2.CAP_PROP_FPS, 50)
        , 'frame height' : (cv2.CAP_PROP_FRAME_HEIGHT, 100 )
        , 'frame width' : (cv2.CAP_PROP_FRAME_WIDTH, 100 )
        }

def print_properties( cap ):
    for k in properties:
        v = properties[k]
        print( "\t Prop %s is %s" % (k,  cap.get( v[0] ) ) )


def main( ):
    cap = cv2.VideoCapture(0 )
    print( 'Before setting' )
    print_properties( cap )
    for k in properties:
        v = properties[k] 
        cap.set( v[0], v[1] )
    print( 'After setting' )
    print_properties( cap )

    N = 0
    start = time.time()
    while True:
        ret, frame = cap.read()
        if ret:
            N += 1
            # cv2.imshow( 'frame', frame )
            # cv2.waitKey( 1 )
        fps = N / ( time.time() - start  )
        if N % 100:
            print("FPS=%f" % fps)

if __name__ == '__main__':
    main()
