#ifndef AVOIDINTERSECTOR_H
#define AVOIDINTERSECTOR_H
 
#include <maya/MArgList.h>
#include <maya/MObject.h>
#include <maya/MGlobal.h>
#include <maya/MPxCommand.h>
 
class AvoidIntersector : public MPxCommand {
 public:
  AvoidIntersector() {};
  virtual MStatus doIt(const MArgList& argList);
  static void* creator();
};
#endif
