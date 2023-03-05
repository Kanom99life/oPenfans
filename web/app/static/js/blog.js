var lastestID = 0;
var curr_email = $("#curr_email").val();
var curr_name = $("#name").val();

$(document).ready(function () {
    (function () {
        $.getJSON("blogentry", blog_table);
    })();
});


$("#addBlogBlog").submit(function (event) {
    // prevent default html form submission action
    event.preventDefault();

    // pack the inputs into a dictionary
    var formData = {};
    $(":input").each(function () {
        var key = $(this).attr('name');
        var val = $(this).val();

        if (key != 'submit') {
            formData[key] = val;
        }

    });

    var $form = $(this);
    var url = $form.attr("action");

    // make a POST call to the back end w/ a callback to refresh the table
    $.post(url, formData, function (blog_data) {
        clearForm();
        refresh_table(blog_data)
        toggleView()

    });
});


function clearForm() {
    $('#addBlogBlog')[0].reset();
    $('#entryid').val('');
};


function blog_table(blog_data) {
    const data = { data: blog_data }
    const creatBlog = ({id, name, message, email, date_created, date_update, avatar_url }) => {
        lastestID = id;
        let date = formatTime(date_created);
        let dateEdit = formatTime(date_update);
        console.log(date_created.split(",")[0])
        const DMY = date_created
        var oldDate = new Date(date_created);
        var editDate = new Date(date_update);

        if(oldDate.getUTCSeconds() === editDate.getUTCSeconds()){
          return currentBlog(id, name, message, email, date, DMY, avatar_url);
        }else{
          return editBlog(id, name, message, email, date, dateEdit, DMY, avatar_url);
        }    
    };

    //console.log(JSON.stringify(data));
    const blog = data.data.map(creatBlog);
    // And add it for each HTML template to the body.
    for (let i = 0; i < blog.length; i++) {
        document.getElementById("blog_display").innerHTML =
            blog[i] + document.getElementById("blog_display").innerHTML;
    }
};


function currentBlog(id, name, message, email, post_date, dateMonthYear, avatar_url){
  return `
      <div class="tweet">
        <div class="row">
    
          <div class="col-md-2 text-center">
            <img src="${avatar_url}" id = "avatar_url${id}" class="tw-user-medium rounded-circle" onclick="openFullscreen(this)">
          </div>
    
          <div class="col-md-10">
            <div class="row tweet-info">
              <div class="col-md-auto">
                <span class="tweet-id" id="id-blog" hidden="hidden">${id}</span>
                <span class="tweet-username" id="name${id}">${name}</span>
                (<span class="tweet-usertag"id="email${id}">${email}</span>)
                <span class="tweet-age" data-text="${dateMonthYear}"> · ${post_date} · <i class="fa-solid fa-earth-asia"></i></span>
              </div>

              <div class="tweet-arrow">
                    <div class="dropdown" >
                    <i class="fa-solid fa-ellipsis" onclick="showDropdownMenu(event)"></i>
                        <div class="dropdown-menu" id ="dropdown_item">
                        ${curr_email === email?
                            `<a class="dropdown-item" href="javascript:void(0) "onclick="prePopulateForm(${id})" >
                                <i class="fa-solid fa-pen" ></i>
                                Edit
                            </a>
                            <a class="dropdown-item" href="javascript:void(0)" onclick="removeItem(${id})">
                                <i class="fa-solid fa-trash"></i>
                                Delete
                            </a>`:
                            `<a class="dropdown-item" href="mailto:${email}?body=Hello%20${name}%20this is a message from%20${curr_name}.">
                                <i class="fa-solid fa-envelope"></i>
                                Send Email
                            </a>`}
                        </div>
                 </div>
              </div>
            </div>
    
              <div class="tweet-text" id="message${id}">${message}</div>

          </div>
        </div>
      </div>`;
};


function editBlog(id, name, message, email, date, edit_date, dateMonthYear, avatar_url){
  return `
      <div class="tweet">
        <div class="row">
    
          <div class="col-md-2 text-center">
          <img src="${avatar_url}" id = "avatar_url${id}" class="tw-user-medium rounded-circle" onclick="openFullscreen(this)">
          </div>
    
          <div class="col-md-10">
            <div class="row tweet-info">
              <div class="col-md-auto">
                <span class="tweet-id" id="id-blog" hidden="hidden">${id}</span>
                <span class="tweet-username" id="name${id}">${name}</span>
                (<span class="tweet-usertag"id="email${id}">${email}</span>)
                <span class="tweet-age" data-text="${dateMonthYear} (Edited ${edit_date} ago)"> · ${date} (edited) · <i class="fa-solid fa-earth-asia"></i> </span>
              </div>
              
              <div class="tweet-arrow">
                    <div class="dropdown" >
                    <i class="fa-solid fa-ellipsis" onclick="showDropdownMenu(event)"></i>
                        <div class="dropdown-menu" id ="dropdown_item">
                        ${curr_email === email?
                            `<a class="dropdown-item" href="javascript:void(0) "onclick="prePopulateForm(${id})" >
                                <i class="fa-solid fa-pen" ></i>
                                Edit
                            </a>
                           <a class="dropdown-item" href="javascript:void(0)" onclick="removeItem(${id})">
                                <i class="fa-solid fa-trash"></i>
                                Delete
                            </a>`:
                            `<a class="dropdown-item" href="mailto:${email}?body=Hello%20${name}%20this is a message from%20${curr_name}.">
                                <i class="fa-solid fa-envelope"></i>
                                Send Email
                            </a>`}
                        </div>
                 </div>
              </div>
            </div>
    
              <div class="tweet-text" id="message${id}">${message}</div>

          </div>
        </div>
      </div>`;

};


function formatTime(date_created) {
    let now = new Date();
    let created = new Date(date_created + " UTC");
    let diff = (now.getTime() - created) / 1000 / 60; // convert to minutes
    diff = Math.abs(Math.round(diff)); // round and get absolute value

    let result;
    if (diff >= 60 && diff < 1440) {
        result = Math.round(diff / 60) + " hours";
    } else if (diff >= 1440) {
        result = new Date(date_created).toLocaleDateString().split(",")[0];
    } else if (diff <= 1) {
        result = "now";
    } else {
        result = diff + " minutes";
    }
    return result;
}


var currentDropdown = null;

function showDropdownMenu(event) {
  var dropdown = event.target.nextElementSibling;
  
  if (dropdown === currentDropdown) {
    // Clicked on the same dropdown that is currently open, so toggle it
    dropdown.style.display = (dropdown.style.display === "block") ? "none" : "block";
  } else {
    // Clicked on a different dropdown, so close the current one (if any) and open the new one
    if (currentDropdown) {
      currentDropdown.style.display = "none";
    }
    dropdown.style.display = "block";
    currentDropdown = dropdown;
  }
  
  document.addEventListener("click", function(event) {
    if (!event.target.matches('.fa-ellipsis') && !event.target.matches('.tw-user-small')) {
      if (currentDropdown) {
        currentDropdown.style.display = "none";
        currentDropdown = null;
      }
    }
  });
}


function removeItem(id) {
  if (!confirm("Are you sure to delete this?")) {
    // console.log("not pass")
    return false;
  }
  
  // console.log("pass")
  var url = "remove_blog"
  var formData = { 'id': id};
  $.post(url, formData, function (blog_data) {
    refresh_table(blog_data)
  });
}


function refresh_table(blog_data) {
  document.getElementById("blog_display").innerHTML = "";
  document
    .getElementById("blog_display")
    .addEventListener("load", blog_table(blog_data));
}


function prePopulateForm(id){
  $('#addBlogBlog')[0].reset();
  $('#name').val(document.getElementById("name"+id).innerHTML)
  $('#email').val(document.getElementById("email"+id).innerHTML)
  $('#message').val(document.getElementById("message"+id).innerHTML)
  $('#entryid').val(id)
  toggleView()
}


function lastestPrePopulateForm(id){
  $('#addBlogBlog')[0].reset();
  $('#name').val(document.getElementById("name"+id).innerHTML);
  $('#email').val(document.getElementById("email"+id).innerHTML);  
}


function toggleView() {
  if ($('#addBlog_display').attr('hidden')) {
    $('#addBlog_display').removeAttr('hidden');
    $('#addBlogBlog').attr('hidden', 'hidden');
  } else {
    $('#addBlog_display').attr('hidden', 'hidden');
    $('#addBlogBlog').removeAttr('hidden');
  }  
}

$("#add_blog").click(function () {
  clearForm();
  toggleView();
  // lastestPrePopulateForm(lastestID)
});

$("#add_blog_notAuth").click(function () {
  clearForm();
  window.location.href = "login";
});

$("#clear_form").click(function () {
  clearForm();
});


$("#cancel_form").click(function () {
  clearForm();
  toggleView();
});


function openFullscreen(img) {
  if (img.requestFullscreen) {
    img.requestFullscreen();
  } else if (img.webkitRequestFullscreen) { /* Safari */
    img.webkitRequestFullscreen();
  } else if (img.msRequestFullscreen) { /* IE11 */
    img.msRequestFullscreen();
  }
}


$("#login").click(function () {
  clearForm();
  window.location.href = "login";
});

$("#signup").click(function () {
  clearForm();
  window.location.href = "signup";
});

$("#logout").click(function () {
  clearForm();
  window.location.href = "logout";
});

$("#editProfile").click(function () {
  clearForm();
  window.location.href = "profile";
});

