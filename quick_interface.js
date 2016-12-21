/******************** IMAGES ********************/
var STONE_IMAGE = 'https://s3.amazonaws.com/files.d20.io/images/26401727/u-v0Ngg7BhDGv0GS5zvuPw/thumb.png?1482011449';
var PINE_IMAGE = 'https://s3.amazonaws.com/files.d20.io/images/26401729/j4FpvNNVnv3aJ4Ky3DdZ1A/thumb.png?1482011451';

/******************** GLOBALS *******************/
var GRID_SIZE = 70; //in pixels
var currentPageID = null;

var createMapToken = function(gridX, gridY, sizeMul, imageSource){
    createObj('graphic', {
       _pageid: currentPageID,
       layer: 'map',
       name: '',
       imgsrc: imageSource,
       width: GRID_SIZE * sizeMul,
       height: GRID_SIZE * sizeMul,
       left: (GRID_SIZE * sizeMul) / 2.0 + GRID_SIZE * gridX,
       top: (GRID_SIZE * sizeMul) / 2.0 + GRID_SIZE * gridY,
    });
    
    log("Create token size " + sizeMul +" at (" + gridX + "," + gridY + ")");
    
}

var processMapTokenMessage = function(msg){
    var params = msg.content.split(',');
        
    if(params.length != 5){
        log("ERROR: Invalid makeMapToken call. Format: !makeMaptoken, gridX, gridY, sizeMul, image");
        return;
    }
    
    var gridX = parseFloat(params[1]);
    var gridY = parseFloat(params[2]);
    var sizeMul = parseFloat(params[3]);
    var image = params[4].trim();
    
    log(params)
    
    if(image == 'STONE_IMAGE'){image = STONE_IMAGE;log(image == STONE_IMAGE)}
    if(image == 'PINE_IMAGE'){image = PINE_IMAGE}
    
    createMapToken(gridX, gridY, sizeMul, image);
}

var setup = function(){
    currentPageID = Campaign().get('playerpageid');
    //currentPage = getObj('page', currentPageID);
    
    //createMapToken(1, 1, 1, STONE_IMAGE)
    

    log('Setting up');
    
    var currentPageMapTokens = findObjs({                              
      _pageid: Campaign().get("playerpageid"),                              
      _type: "graphic",
      layer: 'map',
    });
    _.each(currentPageMapTokens, function(token) {
        log(token.get('name'));
        log(token.get('imgsrc'));
        token.remove();
        //can't delete tokens, so just move them. in future can use a pool of token IDs
    });
}

var processMessage = function(msg) {
    if(msg.type !== "api"){return}
    log(msg);
    if(msg.content == "!setup"){setup()}
    if(msg.content.slice(0, "!makeMapToken".length) == "!makeMapToken"){processMapTokenMessage(msg)}
};

on("ready", function() {
    on("chat:message", function(msg) {if(msg.type == "api"){processMessage(msg)};});
});

