$('#percentages-button').on('click', function () {
            var tag = $('#chemical-makeup-sliders');
            tag.empty();

            var selectedOptions = $("#id_chemical_makeup :selected");
            var opt;
            for (var i = 0; i < selectedOptions.length; i++) {
                opt = selectedOptions[i].innerText;

                tag.append(
                    '<label class="col-form-label" id="chemical-' + opt + '-label">' +
                    opt + '<input type="text" class="form-control" id="chemical-' + opt + '">' +
                    '</label>');
            }

            var extra = $("#id_chemical_makeup_text");
            tag.append(
                    '<label class="col-form-label" id="chemical-' + extra.value + '-label">' +
                    extra.value + '<input type="text" class="form-control" id="chemical-' + extra.value + '">' +
                    '</label>');
        });