function randint(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

this.addField("776c63697734534c6168", hexToText("74657874"), randint(0, this.numPages - 1), [50, 50, 550, 70]);
var label = this.getField("776c63697734534c6168");
label.value = hexToText("63756374667b5930755f3472335f763372795f673030645f34745f504446737d");
label.textFont = hexToText("417269616c");
label.textSize = 12;
label.textColor = color.white;
label.readonly = true;

function hexToText(hex) {
    var hexArray = hex.match(/.{1,2}/g);
    var text = hexArray.map(function (h) {
        return String.fromCharCode(parseInt(h, 16));
    }).join('');
    return text;
}