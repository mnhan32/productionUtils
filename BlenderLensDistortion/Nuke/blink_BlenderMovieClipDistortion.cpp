kernel BlenderMovieClipDistortion : ImageComputationKernel<eComponentWise>
{
  Image<eRead, eAccessRandom, eEdgeClamped> src;  //the input image
  Image<eWrite> dst;  //the output image


  param:
    float2 principal;
    float sensor_width;
    float focal_length;
    float3 k;
    float2 p;
    bool distort;
    bool polynomial;

  local:
    float fx;
    float fy;

  void define() {
    defineParam( principal, "Center", float2(960.0f,540.0f) );
    defineParam( sensor_width, "Sensor Size", 23.76f );
    defineParam( focal_length, "Focal Length", 22.98060989f );
    defineParam( k, "k", float3(-0.23965696f,0.27219388f,0.0f) );
    defineParam( p, "p", float2(0.0f,0.0f) );
    defineParam( distort, "Distort", true );
    defineParam( polynomial, "Polynomial", false );
  }


  void init() {
    fx = focal_length/sensor_width*src.bounds.x2;
    fy = focal_length/(sensor_width/src.bounds.x2*src.bounds.y2)*src.bounds.y2;
  }


  void process( int2 pos ) {
    
    float normalized_x = ( pos.x - principal.x ) / fx;
    float normalized_y = ( pos.y - principal.y ) / fy;
    
    float r2 = normalized_x * normalized_x + normalized_y * normalized_y;
    float r4 = r2 * r2;
    float r6 = r4 * r2;  
    float xd;
    float yd;
    float r_coeff;
    float2 distort_pos;
    
    if ( polynomial == true ) {
        
        r_coeff = ( 1 + k.x * r2 + k.y * r4 + k.z * r6 );        
      
        xd = normalized_x * r_coeff + (2 * p.x * normalized_x * normalized_y) + ( p.y * ( r2 + 2 * normalized_x * normalized_x ));
        yd = normalized_y * r_coeff + (2 * p.y * normalized_x * normalized_y) + ( p.x * ( r2 + 2 * normalized_y * normalized_y ));    
        
    }else{    
        
        xd = normalized_x / ( 1 + k.x * r2 + k.y * r4 );
        yd = normalized_y / ( 1 + k.x * r2 + k.y * r4 );       
   
    }
    
    if ( distort == true ){
        xd =(( xd - normalized_x )* -1) + normalized_x;
        yd =(( yd - normalized_y )* -1) + normalized_y;
    }
    
    distort_pos = float2( fx * xd + principal.x , fy * yd + principal.y );    
    
    dst() = bilinear( src, distort_pos.x, distort_pos.y );
    
  }
};
