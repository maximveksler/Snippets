import maya.cmds as cmds
import maya.mel as mel

def stacksHandler(object):
	"""
	This decorator is used to handle various Maya stacks.

	@param object: Python object. ( Object )
	@return: Python function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This decorator is used to handle various Maya stacks.

		@return: Python object. ( Python )
		"""

		cmds.undoInfo(openChunk=True)
		value = object(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya produces a weird command error if not wrapped here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")"% (__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def unfoldBandUVs(object, divisions=1, history=True):
	"""
	This definition unfold object band UVs.

	@param object: Object. ( String )
	@param divisions: Extrusion divisions. ( Integer )
	@param history: Keep construction history. ( Boolean )
	"""

	edgesCount = cmds.polyEvaluate(object, edge=True)
	edges = cmds.ls(object +".e[0:" + str(edgesCount-1) + "]", fl=True, l=True)

	cmds.select(object)
	cmds.polySelectConstraint(m=3, t=0x8000, w=1)
	cmds.polySelectConstraint(m=0)
	for i in range(divisions):
		mel.eval("GrowPolygonSelectionRegion();")
	bandEdges = cmds.ls(sl=True, fl=True, l=True)
	bandFaces = cmds.ls(cmds.polyListComponentConversion(bandEdges, fe=True, tf=True), fl=True)
	cmds.select(bandFaces)
	cmds.polyForceUV(unitize=True)
	cmds.polySelectConstraint(m=3, t=0x8000, sm=1)
	seamsEdges = cmds.ls(sl=True, fl=True, l=True)
	weldEdges = list(set(bandEdges).difference(set(seamsEdges)))
	cmds.polyMapSewMove(weldEdges)
	cmds.polyLayoutUV(bandFaces, scale=1, rotateForBestFit=0, layout=1)
	uvs = cmds.polyListComponentConversion(bandFaces, toUV=1)
	cmds.polyEditUV(uvs, u=1, v=0)

	not history and cmds.delete(object, ch=True)

@stacksHandler
def unfoldBand_button_OnClicked(state=None):
	"""
	This definition is triggered by the unfoldBand_button button when clicked.

	@param state: Button state. ( Boolean )
	"""

	for object in cmds.ls(sl=True, l=True, o=True):
		unfoldBandUVs(object, divisions=cmds.intSliderGrp("divisions_intSliderGrp", q=True, v=True), history=cmds.checkBox("keepConstructionHistory_checkBox", q=True, v=True))

def unfoldBand_window():
	"""
	This definition creates the 'Unfold Band' main window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("unfoldBand_window", exists=True)):
		cmds.deleteUI("unfoldBand_window")

	cmds.window("unfoldBand_window",
		title="Unfold Band",
		width=384)

	spacing=5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.separator(height=10, style="singleDash")

	cmds.intSliderGrp("divisions_intSliderGrp", label="Divisions", field=True, minValue=0, maxValue=10, fieldMinValue=0, fieldMaxValue=65535, value=2)

	cmds.separator(style="single")

	cmds.columnLayout(columnOffset=("left", 140) )
	cmds.checkBox("keepConstructionHistory_checkBox", label="Keep Construction History",  v=True)
	cmds.setParent(topLevel=True)

	cmds.separator(height=10, style="singleDash")

	cmds.button("unfoldBand_button", label="Unfold Band!", command=unfoldBand_button_OnClicked)

	cmds.showWindow("unfoldBand_window")

	cmds.windowPref(enableAll=True)

def unfoldBand():
	"""
	This definition launches the 'Unfold Band' main window.
	"""

	unfoldBand_window()

@stacksHandler
def IUnfoldBand():
	"""
	This definition is the unfoldBand definition Interface.
	"""

	unfoldBand()
