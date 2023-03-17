var lastestID = 0;
var curr_email = $("#curr_email").val();
console.log(curr_email)
var curr_name = $("#name").val();


$(document).ready(function () {
    (function () {
        $.getJSON("blogentry", blog_table); //user_blogentry
    })();
});


$("#addBlogBlog").submit(function (event) {
    // prevent default html form submission action
    event.preventDefault();

    // pack the inputs into a dictionary
    const formData = new FormData();

    $("#addBlogBlog :input").each(function () {
      var key = $(this).attr('name');
      var val = $(this).val();

      if(key === 'image'){
        var files = $(this)[0].files[0];
        formData.append('image', files);
      }

        if (key != 'submit' && key != 'image') {
            formData.append(`${key}`,val);
        }

    });

    /*for (let obj of formData) {
      console.log(obj);
    }*/

    var $form = $(this);
    var url = $form.attr("action");

    // make a POST call to the back end w/ a callback to refresh the table
    $.ajax({
      url: url,
      type: 'post',
      data: formData,
      contentType: false,
      processData: false,
      success: function(blog_data){
        clearForm();
        refresh_table(blog_data)
        toggleView()
      },
  });
});


function clearForm() {
    $('#addBlogBlog')[0].reset();
    $('#entryid').val('');
};


function blog_table(blog_data) {
    const data = { data: blog_data }
    const creatBlog = ({id, name, message, email, date_created, date_update, avatar_url, img, can_read, owner_id}) => {
        url = "/user/";
        curr_url ="/yourblog";
        lastestID = id;
        let date = formatTime(date_created);
        let dateEdit = formatTime(date_update);
        console.log(date_created.split(",")[0])
        const DMY = date_created
        var oldDate = new Date(date_created);
        var editDate = new Date(date_update);


        if(oldDate.getUTCSeconds() === editDate.getUTCSeconds()){
            return currentBlog(id, name, message, email, date, DMY, avatar_url, url, img, can_read, owner_id);
        } else{
            return editBlog(id, name, message, email, date, dateEdit, DMY, avatar_url, url, img, can_read, owner_id);
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


function currentBlog(id, name, message, email, post_date, dateMonthYear, avatar_url, url, img, can_read, owner_id){
  console.log(can_read);
  return `
      <div class="tweet">
        <div class="row">
    
          <div class="col-md-2 text-center">
            <img src="${avatar_url}" id = "avatar_url${id}" class="tw-user-medium rounded-circle">
          </div>
    
          <div class="col-md-10">
            <div class="row tweet-info">
              <div class="col-md-auto">
                <span class="tweet-id" id="id-blog" hidden="hidden">${id}</span>
                <!--<span class="tweet-username" id="name${id}"><a href="${url}${name}">${name}</a></span> -->
                ${curr_email === email?
                `<a class="tweet-username" id="name${id}" href="${curr_url}">${name}</a>`:
                `<a class="tweet-username" id="name${id}" href="${url}${email}">${name}</a>`}
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
            ${ can_read ?
              `<div class="tweet-text" id="message${id}">${message}</div>
              ${ img ? 
              `<div class="tweet-text">
                <img style="max-width: 75%" src="/images/${img}/${owner_id}" />
              </div>` : ``
              }` : `<div style="background-color: #f2f2f2; padding: 10px; text-align: center; width: 94%;">
              <p style="display: inline-block; padding-top: 10px; padding-bottom: 10px; border-radius: 10px; ">
                <i class="fas fa-lock" style="font-size: 3em;"></i>
                <br>
                <span style="font-size: 1.2em; font-family: Bree Serif, serif;">This account is private, please subscribe to unlock the content.</span>
              </p>
            </div>
            `
            }
              
          </div>
        </div>
      </div>`;
};


function editBlog(id, name, message, email, date, edit_date, dateMonthYear, avatar_url , url, img, can_read, owner_id){
  console.log(can_read)
  return `
      <div class="tweet">
        <div class="row">
    
          <div class="col-md-2 text-center">
          <img src="${avatar_url}" id = "avatar_url${id}" class="tw-user-medium rounded-circle" >
          </div>
    
          <div class="col-md-10">
            <div class="row tweet-info">
              <div class="col-md-auto">
                <span class="tweet-id" id="id-blog" hidden="hidden">${id}</span>
                ${curr_email === email?
                  `<a class="tweet-username" id="name${id}" href="${curr_url}">${name}</a>`:
                  `<a class="tweet-username" id="name${id}" href="${url}${email}">${name}</a>`}
                <span class="tweet-age" data-text="${dateMonthYear} (Edited ${edit_date})"> · ${date} (edited) · <i class="fa-solid fa-earth-asia"></i> </span>
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
              ${ can_read ?
                `<div class="tweet-text" id="message${id}">${message}</div>
                ${ img ? 
                `<div class="tweet-text">
                  <img style="max-width: 75%" src="/images/${img}/${owner_id}" />
                </div>` : ``
                }` : `<div style="background-color: #f2f2f2; padding: 10px; text-align: center; width: 94%;">
                <p style="display: inline-block; padding-top: 10px; padding-bottom: 10px; border-radius: 10px; ">
                  <i class="fas fa-lock" style="font-size: 3em;"></i>
                  <br>
                  <span style="font-size: 1.2em; font-family: Bree Serif, serif;">This account is private, please subscribe to unlock the content.</span>
                </p>
              </div>
              `
              }
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
        result = Math.round(diff / 60) + " hours ago";
    } else if (diff >= 1440) {
        result = new Date(date_created).toLocaleDateString().split(",")[0];
    } else if (diff <= 1) {
        result = "now";
    } else {
        result = diff + " minutes ago";
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
  //$('#email').val(document.getElementById("email"+id).innerHTML)
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


$("#editBut").click(function () {
  clearForm();
});

$("#google-login").click(function () {
  
  window.location.href = "google/auth/";
});
