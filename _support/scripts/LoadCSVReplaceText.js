/*
if(app.documents.length > 0){
    alert("There are " + app.documents.length + " open documents");
}else{
    alert("There are no open documents");
}
*/

#target photoshop  
app.bringToFront();  

//main();  

// FUNCTIONS

//if(!documents.length) return;  
////////////////////////////////////////////////////////////////////  
//hard code your csv file  
//var CSVfile = File("/c/folderWhatever/fileName.csv");  
/////// remove this code when file is hard coded  
// Prompt for SAVE SLUG and OUTPUT LOCATION

var outputFolder = Folder.selectDialog( "Please select output folder");
var nameSlug = prompt("Please type a SLUG to prepend to the filename.","","Input your text here");


var CSVfile = null;  
while(CSVfile == null){  
CSVfile = File.openDialog("Please select CSV file.","CSV File:*.csv");   
}  
//////////////////////////////////////////////////////  
CSVfile.open('r');  
var Data=[];  
while(!CSVfile.eof){  
    Line = CSVfile.readln(); 
    //if (Line.length > 0) Data.push(Line.toUpperCase());   
    if (Line.length > 0) {
        text = Line.toUpperCase();

        if(app.documents.length != 0){
            var doc = app.activeDocument;
            
            for(i = 0; i < doc.artLayers.length; ++i){
                var layer = doc.artLayers[i];
            
                if(layer.kind == LayerKind.TEXT){
                    // layer.textItem.font = "ArialMT"; // <---- Can set the font here if we desire.
                    layer.textItem.contents = text; // Use += to append
                }
            }
        }


        // SAVE THE FILE
        var saveFile = new File(outputFolder + "/" + nameSlug.toLowerCase() + text.toLowerCase() + ".png"); //amend ext to suit
        savePNG(saveFile); //amend to suit
    }  

}  


//var lineLength = Line.length;
//for (var i = 0; i < lineLength; i++) {
//    alert(Line[i]);
    //Do something
//} ^^ Not needed with the WHILE loop above, we can save


if(app.documents.length != 0){
    var doc = app.activeDocument;
    
    for(i = 0; i < doc.artLayers.length; ++i){
        var layer = doc.artLayers[i];
    
        if(layer.kind == LayerKind.TEXT){
            // layer.textItem.font = "ArialMT"; // <---- Can set the font here if we desire.
            layer.textItem.contents = "Envato"; // Use += to append
        }
    }
}






function savePNG(saveFile){ //amend to suit
    pngSaveOptions = new PNGSaveOptions()
    pngSaveOptions.compression=1 //(level of compression 0 .. 9 0 - without compression)
    pngSaveOptions.interlaced=false
    activeDocument.saveAs(saveFile, pngSaveOptions, true, Extension.LOWERCASE);
};

// END FUNCTIONS

// This replaces all of the text.












// Other Functions for future changes? From here: https://stackoverflow.com/questions/14571008/photoshop-scripting-changing-text-of-a-text-layer

function getTextLayer(target) {
    // this basically loops all the layers to find the
    // upmost text layer with the content #nn... and returns it
        if (target == null) return false;
        var layers      = target.layers,
            layerLen    = layers.length;
        for (var i = 0; i < layerLen; i++) {
            var layer       = layers[i],
                isLayerSet  = layer.typename == 'LayerSet',
                isValid     = layer.kind == LayerKind.TEXT &&
                              /^\s*#\d+\s*$/.test(layer.textItem.contents);
                // we're allowing spaces around the text just in case
            if (!isLayerSet && !isValid) continue;
            if (isLayerSet) {
                var found = getTextLayer(layer);
                if (found) return found;
            } else return layer;
        }
        return false;
    }