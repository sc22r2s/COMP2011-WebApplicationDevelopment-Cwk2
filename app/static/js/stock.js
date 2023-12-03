var batch = { batchCode: "", batchDirection: "0", productDetail: [] };
var batchProducts = [];

$("#ProductCodeInput").keydown(function (event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    var code = $("#ProductCodeInput").val();

    $.ajax({
      type: "GET",
      url: "/ajax/display-product-detail",
      data: { productCode: code },
      success: function (data, status, xhr) {
        if (data.hasOwnProperty("error")) {
          alert("Invalid product code");

          // Clear data from form after appending data in table
          clearProductDetail();
        } else {
          // Add data to the form
          $("#ProductIdDisplay").val(data.id);
          $("#ProductNameDisplay").val(data.productName);
          $("#ProductDescriptionDisplay").val(data.description);
          $("#ProductRateDisplay").val(data.rate);
          // Next cursor destination
          $("#ProductQuantityInput").focus();
        }
      },
      error: function (jqXhr, textStatus, errorMessage) {
        // error callback
        alert(errorMessage);
      },
    });
  }
});

$("form").on("submit", function (event) {
  event.preventDefault();
  if ($("#ProductNameDisplay").val() === "") {
    // Check if product code has been entered
    alert("Enter product code");
  } else if ($("#ProductQuantityInput").val() === "") {
    // Check if product quantity has been entered
    alert("Enter product quantity");
  } else if (!parseInt($("#ProductQuantityInput").val())) {
    // Check if product quantity is an integer
    alert("Invalid product quantity");
  } else if (batchProducts.includes(parseInt($("#ProductIdDisplay").val()))) {
    // Check if product already in batch
    alert("Product already added in this batch");
  } else {
    // Append data in the table
    $("#product-row").append(
      "<tr><td>" +
        $("#ProductIdDisplay").val() +
        "</td><td>" +
        $("#ProductCodeInput").val() +
        "</td><td>" +
        $("#ProductNameDisplay").val() +
        "</td><td>" +
        $("#ProductQuantityInput").val() +
        "</td><td><button type='button' class='btn btn-light' onclick='removeRow(this, " +
        $("#ProductIdDisplay").val() +
        ")'>Delete<i class='far fa-trash-alt'></i></button></td></tr>"
    );

    batch["productDetail"].push({
      productId: parseInt($("#ProductIdDisplay").val()),
      quantity: parseInt($("#ProductQuantityInput").val()),
    });
    batchProducts.push(parseInt($("#ProductIdDisplay").val()));

    // Clear data from form after appending data in table
    clearProductDetail();

    // Next cursor destination
    $("#ProductCodeInput").focus();
  }
});

// Clear all fields related to product
function clearProductDetail() {
  $("#ProductCodeInput").val("");
  $("#ProductIdDisplay").val("");
  $("#ProductNameDisplay").val("");
  $("#ProductDescriptionDisplay").val("");
  $("#ProductRateDisplay").val("");
  $("#ProductQuantityInput").val("");
}

// Remove the row and also remove from the json objects
function removeRow(btndel, pId) {
  if (typeof btndel == "object") {
    if (removeProductFromBatch(pId)) $(btndel).closest("tr").remove();
  } else {
    return false;
  }
}

// Remove pId from batch and batchProducts
function removeProductFromBatch(pId) {
  // find the index position
  const requiredIndex = batch["productDetail"].findIndex((el) => {
    return el.productId === pId;
  });
  if (requiredIndex === -1) {
    return false;
  }

  // also remove item from batchProducts
  const idx = batchProducts.indexOf(pId);
  if (idx > -1) {
    // only splice array when item is found
    batchProducts.splice(idx, 1); // remove one item only, which should be the found pId at the index
  }

  // remove from batch
  return !!batch["productDetail"].splice(requiredIndex, 1);
}

// Call ajax to save the batch
function saveBatch() {
  if (batchProducts.length === 0) {
    alert("No product added");
  } else if ($("#BatchCodeInput").val() === "") {
    alert("Batch code must be provided");
  } else {
    batch["batchCode"] = $("#BatchCodeInput").val();
    batch["batchDirection"] = $("#StockInOut").val();

    $.ajax({
      type: "GET",
      url: "/ajax/add-batch",
      data: { batch: JSON.stringify(batch) },
      success: function (data, status, xhr) {
        if (data.hasOwnProperty("error")) {
          alert("Batch can not be added");
        } else {
          alert("Batch added successfully");
          location.reload();
        }
      },
      error: function (jqXhr, textStatus, errorMessage) {
        // error callback
        alert(errorMessage);
      },
    });
  }
}
