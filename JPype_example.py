"""
An example of Python accessing Java class libraries via JPype

@author Tomas Lazauskas, 2016
@web www.lazauskas.net
@email tomas.lazauskas[a]gmail.com
"""

import os

import jpype
from jpype import *

import messages

class JPypeInterface:
  """
  """
  
  def __del__(self):
    """
    Destructor.
    
    """

    self.__shutdownJVM()
  
  def __init__(self, options=None, args=None, standAlone=True):
    """
    Constructor.
    
    """
    
    self._globJVMOn = False
    self._globJVMJar = None
        
    self._globJVMOutPath = "jvm.out"
    self._globJVMErrPath = "jvm.err"

    self.__startJVM()
  
  def __startJVM(self):
    """
    Initializes Java Virtual Machine and loads symmetrizer
    """
    
    # Path to the jar file
    jarpath = os.path.join(None)
    
    try:
      jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % (jarpath))
      
      self._globJVMOn = True
      self._globJVMJar = JPackage('net.webmo.symmetry').Main
      messages.log(__name__, "JVM initialised!", verbose=1)
      
      # Hello world from Java
      jpype.java.lang.System.out.println("Java: hello world!")
      
      #TODO: In future this should be done via streams
      fs = jpype.JClass("java.io.File")
      ps = jpype.JClass("java.io.PrintStream")
      
      # Directing the output
      jpype.java.lang.System.setOut(ps(fs(self._globJVMOutPath)))
      jpype.java.lang.System.setErr(ps(fs(self._globJVMErrPath)))

    except:
      self._globJVMOn = False
      self._globJVMJar = None
      
      messages.warning(__name__, "Cannot start JVM!", verbose=0)
          
  def __shutdownJVM(self):
    """
    Shuts down the Java Virtual Machine.
    
    """
    
    if self._globJVMOn:
      jpype.shutdownJVM()
      
      self._globJVMOn = False
      self._globJVMJar = None
      
      messages.log(__name__, "JVM shut down!", verbose=1)
      
      self._clearJVMOutputFiles()
  
  def _clearJVMOutputFiles(self):
    """
    Deletes JVM output files.
    
    """
    
    try:
      os.unlink(self._globJVMOutPath)
      os.unlink(self._globJVMErrPath)
      
    except:
      messages.warning(__name__, "Cannot remove JVM output files!", verbose=1)
  
  def run(self):
    """
    The main run routine
    
    """
  
    self._clearJVMOutputFiles()

if __name__ == "__main__":
  # Runs the selected jar module 
  
  jInterface = JPypeInterface()

