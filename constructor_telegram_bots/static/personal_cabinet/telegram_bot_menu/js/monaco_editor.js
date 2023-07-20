const updateMonacoEditorHeight = (monacoEditor) => {
	monacoEditor.layout({height: monacoEditor.getContentHeight()});
	monacoEditor.layout();
}