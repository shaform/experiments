function getSurveyData(sheetName) {
  var arrayOfArrays = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName || 'survey').getDataRange().getValues();
  var headers = arrayOfArrays.shift();
  return arrayOfArrays;
}

function getUrlData(sheetName) {
  var arrayOfArrays = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName || 'urls').getDataRange().getValues();
  var headers = arrayOfArrays.shift();
  var mapOfUrls = {};
  for (var i=0; i<arrayOfArrays.length; i+=1) {
    var h = arrayOfArrays[i][0];
    var url = arrayOfArrays[i][1];
    mapOfUrls[h] = url;
  }
  return mapOfUrls;
}

function makeOurForm() {
  var title = 'Dogs vs. Cats Survey';
  var desc = 'Please select the picture that looks like a cat.';
  var mapOfUrls = getUrlData();
  var surveyData = getSurveyData();
  
  var form = FormApp.create(title)
  form.setDescription(desc);
  for (var i=0; i<surveyData.length; i++) {
    Utilities.sleep(10);
    var item = form.addMultipleChoiceItem();
    item.setTitle('Q' + surveyData[i][0] + ': Which one looks like a cat?')
    .setChoices([
      item.createChoice('1'),
      item.createChoice('2')
    ])
    .setRequired(true);
    
    for (var j=1; j<surveyData[i].length; j++) {
      var name = '(' + j + ')';
      var h = surveyData[i][j];
      var img = UrlFetchApp.fetch(mapOfUrls[h]);
      Utilities.sleep(100);
      var imgItem = form.addImageItem();
      try {
        imgItem.setTitle(name).setImage(img);
      } catch (e) {
        Utilities.sleep(500);
        imgItem.setTitle(name).setImage(img);
      }
    }
  }
}
