#include "AvoidIntersectorCmd.h"
#include <maya/MFnPlugin.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>
#include <maya/MFnMesh.h>
#include <maya/MFn.h>
#include <maya/MMatrix.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MDoubleArray.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MTypes.h>
#include <maya/MVector.h>
#include <maya/MItSelectionList.h>
#include <maya/MIOStream.h>
#include <ctime>

void* AvoidIntersector::creator() { return new AvoidIntersector; }

MStatus AvoidIntersector::doIt(const MArgList& argList) {    
    
    std::clock_t start = clock();
    cout << "Running Avoid Intersect." << endl;
    
    /* get selection data in iter list*/
    MSelectionList sel;
    MStatus status = MGlobal::getActiveSelectionList( sel );
    
    /*get mesh data, mesh is selected last*/
    MDagPath mesh;
    sel.getDagPath( sel.length()-1, mesh );
    MFnMesh fnMesh( mesh );
    
    /*Selection list iterator, filtering out non nurbs curve*/
    MItSelectionList iter( sel );
    iter.setFilter( MFn::kNurbsCurve );
    iter.reset();
  
    for ( ; !iter.isDone(); iter.next() )
    {
        MDagPath cPath;
        iter.getDagPath( cPath );
        MMatrix iMat = cPath.inclusiveMatrix();
        
        MFnNurbsCurve fnCurve( cPath );
        MDoubleArray knts;
        fnCurve.getKnots( knts );
        
        /*point array to store all end point data in a curve*/
        MPointArray eps;
        
        int count = 0;
        for( unsigned int i = 0; i < knts.length()-4; i++){ 
            MPoint pnt;
            MPoint wPnt;
            MPoint cPnt;
            MVector cNormal;
            MVector toPnt;
            
            /*get point world poision from knot param*/
            fnCurve.getPointAtParam( i, pnt);
            wPnt = pnt * iMat;
            
            /*get closest pos and normal, use dot product to check if point is inside or outside*/
            fnMesh.getClosestPointAndNormal( wPnt, cPnt, cNormal, MSpace::kWorld );
            toPnt = wPnt - cPnt;
            toPnt.normalize();            
            double dotPnt = toPnt * cNormal;
            
            if( dotPnt < 0 ){
                    
                    /*if inside, move point to closest point*/
                    count ++;
                    wPnt = cPnt;
                    /*if not root ep, push along normal (away from mesh)*/
                    if ( i > 2 ){   
                                      
                        wPnt += 0.05 * toPnt;                        
                    }
            
            }
            /*store point array data in eps*/
            eps.append( wPnt );
            
        }
        
        if( count > 0 ){
            /*if inside detected for any knot, draw new curve with eps data*/
            MFnNurbsCurve nCurve;
            nCurve.createWithEditPoints( eps, fnCurve.degree(), fnCurve.form(), false, true, false);
           
        }
                
    }
  
    cout << "Finish AvoidIntersect in : " << clock() - start << endl;
    return MS::kSuccess;
}

MStatus initializePlugin(MObject obj) {
    MFnPlugin plugin(obj, "Menghan Ho", "1.0", "Any");
    MStatus status = plugin.registerCommand("avoidIntersect", AvoidIntersector::creator);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    return status;
}
 
MStatus uninitializePlugin(MObject obj) {
    MFnPlugin plugin(obj);
    MStatus status = plugin.deregisterCommand("avoidIntersect");
    CHECK_MSTATUS_AND_RETURN_IT(status);
    return status;
}
