// Disable the autoDiscover feature
// Read more: https://docs.dropzone.dev/getting-started/setup/declarative
Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;
        
        var url = "http://127.0.0.1:5000/classify_image";

        // the $.post() method requests data from the server using an HTTP POST request
        $.post(url, {
            image_data: file.dataURL
        },function(data, status) {
            /* 
            Below is a sample response for detecting two faces in an image
            data = [
                {
                    class: "tom_holland",
                    class_probability: [1.05, 12.67, 22.00, 4.5, 91.56],
                    class_dictionary: {
                        "chris_evans": 0,
                        "tom_holland": 1,
                        "mark_ruffalo": 2, 
                        "scarlett_johansson": 3, 
                        "robert_downey_jr": 4, 
                        "chris_hemsworth": 5
                    }
                },
                {
                    class: "scarlett_johansson",
                    class_probability: [7.02, 23.7, 52.00, 6.1, 1.62],
                    class_dictionary: {
                        "chris_evans": 0,
                        "tom_holland": 1,
                        "mark_ruffalo": 2, 
                        "scarlett_johansson": 3, 
                        "robert_downey_jr": 4, 
                        "chris_hemsworth": 5
                    }
                }
            ]
            */
            console.log(data);

            // Case 1: No face detected from image -> display an error
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }

            let match = null;
            let bestScore = -1;

            // Case 2: Face(s) are detected from the image, pick the face with highest prob
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                if(maxScoreForThisClass>bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`[data-avenger="${match.class}"]`).html());
                let classDictionary = match.class_dictionary;

                for(let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let proabilityScore = match.class_probability[index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(proabilityScore);
                }
            }
            // dz.removeFile(file);            
        });
    });

    $("#submitBtn").on('click', function (e) {
        // upload the file that's currently queued
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});

