// gnarly_status.js

// ----------------------------------------------------------------------------
// Defaults for display
// let FONT_SIZE = 14;
// let DISPLAY_HEIGHT = 135;
// let DISPLAY_WIDTH = 240;
// let NEW_LINE = FONT_SIZE + 2;

const BLACK = "#000000";
const WHITE = "#FFFFFF";
const ORANGE = "#FFA500";
const MAGENTA = "#FF00FF";
const CYAN = "#00FFFF";
const RED = "#FF0000";
const GREEN = "#00FF00";
const BLUE = "#0000FF";
const YELLOW = "#FFFF00";
const LIGHT_GREEN = "#20A020";
const PURPLE = "#800080";

const TIME_COLOR = BLACK;
const FILE_COLOR = YELLOW;
const COPY_COLOR = RED;
const SD_COLOR = MAGENTA;
const HD_COLOR = CYAN;

const DISPLAY_ROWS = 7;
// Cache for progress bar values to avoid unnecessary updates
let progressBarCache = {};
// ----------------------------------------------------------------------------
function basename(path) {
  if (!path || typeof path !== "string") {
    return "";
  }
  // Extracts the base name from a file path
  return path.split("/").pop().split("\\").pop();
}

// ----------------------------------------------------------------------------
function cls() {
  for (let line = 0; line <= DISPLAY_ROWS; line++) {
    const lineid = `line${line}`;
    ele = document.getElementById(lineid);
    if (ele) {
      ele.style.backgroundColor = BLACK;
      ele.innerHTML = "&nbsp;";
    }
  }
  // update_display( data._epoch);
}

// ----------------------------------------------------------------------------
function print_line(
  txt,
  line = 2,
  color = WHITE,
  txt2 = "",
  bg = BLACK,
  justify = "left",
) {
  const lineid = `line${line}`;
  ele = document.getElementById(lineid);
  if (ele) {
    ele.style.color = color;
    ele.style.backgroundColor = bg;
    ele.style.textAlign = justify;
    ele.innerHTML = txt + (txt2 ? ` ${txt2}` : "");
  }
}

// ----------------------------------------------------------------------------
function center_line(txt, line = 2, color = WHITE, bg = BLACK) {
  print_line(txt, line, color, "", bg, "center");
}

// ----------------------------------------------------------------------------
function show_progress_bar(
  text,
  elementId,
  progress,
  color = WHITE,
  bg = BLACK,
) {
  const ele = document.getElementById(elementId);
  if (ele) {
    ele.style.color = color;
    ele.style.backgroundColor = bg;
    const percent = Math.round(Math.min(Math.max(progress * 100, 0), 100)) || 0;

    // Check cache to avoid unnecessary updates
    const cacheKey = elementId;
    const lastValues = progressBarCache[cacheKey];
    if (
      lastValues &&
      lastValues.text === text &&
      lastValues.percent === percent
    ) {
      return; // No change, skip update
    }

    // Check if progress bar is already initialized
    let progressEl = ele.querySelector("progress");
    let textEl = ele.querySelector(".progress-text");
    let percentEl = ele.querySelector(".progress-percent");
    // Initialize the HTML structure
    // Add a style block for progress element
    const styleId = `${elementId}_style`;
    let styleEle = document.getElementById(styleId);
    if (!styleEle) {
      styleEle = document.createElement("style");
      styleEle.id = styleId;
      document.head.appendChild(styleEle);
    }

    // Custom progress bar styling
    styleEle.textContent = `
        #${elementId} progress {
          -webkit-appearance: none;
          appearance: none;
        }
        #${elementId} progress::-webkit-progress-bar {
          background-color: ${bg};
        }
        #${elementId} progress::-webkit-progress-value {
          background-color: ${color};
        }
        #${elementId} progress::-moz-progress-bar {
          background-color: ${color};
        }
      `;

    ele.innerHTML = `
        <div style="display: flex; align-items: left; width: 100%;">
          <div style="width: 5%;">&nbsp;</div>
          <div class="progress-text" style="width: 10%; color: ${color}; text-align: left;">${text}</div>
          <div class="progress-percent" style="width: 11%; color: ${color}; text-align: left;">${percent}%</div>
          <progress 
            max="100" 
            value="${percent}"   
            style="width: 69%; height: 0.8rem;">
          </progress>
        </div>
      `;

    // Update cache
    progressBarCache[cacheKey] = { text, percent };
  }
}

// ----------------------------------------------------------------------------
function update_display(epoch_seconds) {
  center_line(new Date(epoch_seconds * 1000).toLocaleTimeString(), 0);
}

// ----------------------------------------------------------------------------
function show_copy(percent, line = 1) {
  show_progress_bar("Copy", `line${line}`, percent, COPY_COLOR);
}

// ----------------------------------------------------------------------------
function show_files(percent, line = 2) {
  show_progress_bar("Files", `line${line}`, percent, FILE_COLOR);
}

// ----------------------------------------------------------------------------
function show_sd(percent, line = 3) {
  show_progress_bar("SD", `line${line}`, percent, SD_COLOR);
}

// ----------------------------------------------------------------------------
function show_hd(percent, line = 4) {
  show_progress_bar("HD", `line${line}`, percent, HD_COLOR);
}

// ----------------------------------------------------------------------------
function show_file_stats(filenum, total) {
  print_line("&nbsp;&nbsp;File", 6, WHITE, `${filenum} / ${total}`);
}

// ----------------------------------------------------------------------------
function show_tx_stats(filename, bps) {
  bps = parseInt(bps);
  let bpsStr = bps;
  if (bps >= 1024 * 1024) {
    bpsStr = `${parseInt(bps / (1024 * 1024))}M`;
  } else if (bps >= 1024) {
    bpsStr = `${parseInt(bps / 1024)}K`;
  }
  center_line(`${bpsStr}b/s`, 7, WHITE, BLUE);
}

function show_remain_stats(left) {
  print_line("&nbsp;&nbsp;Left", 6, WHITE, left);
}

// ----------------------------------------------------------------------------
// Status Handlers

// ----------------------------------------------------------------------------
function status_error(topic, data) {
  cls();

  let msg = "Error";
  if ("level" in data) {
    msg += `:${data.level}`;
  }
  center_line(msg, 0, WHITE, RED);
  center_line(data.msg, 1, WHITE);
  if ("msg2" in data && data.msg2 && data.msg2.length) {
    center_line(data.msg2, 3, RED);
  }
  update_display(data._epoch);
}

// ----------------------------------------------------------------------------
function status_ready(topic, data) {
  center_line("Insert SD card", 2, GREEN);
  update_display(data._epoch);
}

// ----------------------------------------------------------------------------
function status_startcopy(topic, data) {
  cls();
  update_display(data._epoch);
}

// ----------------------------------------------------------------------------
function status_endcopy(topic, data) {
  cls();
  update_display(data._epoch);
}

let start_copy_time = 0;

// ----------------------------------------------------------------------------
function status_copydata(topic, data) {
  let elapsed = 0;
  if (data.size) {
    show_copy(data.copied / data.size);
  }
  show_files(data.files_copied / data.files_total);

  if (data.rsync) {
    const left = data.files_total - data.files_copied;
    show_remain_stats(left);
  } else {
    show_file_stats(data.files_copied, data.files_total);
  }

  if (!data.copied) {
    start_copy_time = Date.now() / 1000;
  } else {
    elapsed = Date.now() / 1000 - start_copy_time;
  }
  let bps = data.bps || parseInt(data.copied / (elapsed || 1));
  const filename = basename(data?.fromfile ?? "");
  show_tx_stats(filename, bps);
  update_display(data._epoch);
}

// ----------------------------------------------------------------------------
function status_waitremove(topic, data) {
  cls();
  center_line("Remove SD Card", 2, ORANGE);
  update_display(data._epoch);
}

// ----------------------------------------------------------------------------
function quick_perc(free, size) {
  return (size - free) / size;
}

// ----------------------------------------------------------------------------
function status_devicedata(topic, data) {
  if (data.sd_size) {
    show_sd(quick_perc(data.sd_free, data.sd_size));
  }
  if (data.hd_size) {
    show_hd(quick_perc(data.hd_free, data.hd_size));
  }
  update_display(data._epoch);
}

// ----------------------------------------------------------------------------
function status_diskfull(topic, data) {
  // cls();
  center_line("HD disk full", 2, WHITE, RED);
  update_display(data._epoch);
}

// ----------------------------------------------------------------------------
function status_fivelines(topic, data) {
  let color = LIGHT_GREEN;
  cls();
  if ("color" in data && data.color) {
    color = data.color;
  }

  for (let line = 0; line < Math.min(5, data.lines.length); line++) {
    const content =
      !data.lines[line] || !data.lines[line].length
        ? "&nbsp;"
        : data.lines[line];
    center_line(content, line, color);
  }

  update_display(data._epoch);
}

// ----------------------------------------------------------------------------
function status_keepalive(topic, data) {
  update_display(data._epoch);
}

// ----------------------------------------------------------------------------
function status_cls(topic, data) {
  cls();
  update_display(data._epoch);
}

// ----------------------------------------------------------------------------
function null_handler(topic, data) {
  // Do nothing
}

// ----------------------------------------------------------------------------
function handle_msg(topic, data) {
  const handlers = {
    "/photos/error": status_error,
    "/photos/ready": status_ready,
    "/photos/startcopy": status_startcopy,
    "/photos/endcopy": status_endcopy,
    "/photos/copydata": status_copydata,
    "/photos/waitremove": status_waitremove,
    "/photos/devicedata": status_devicedata,
    "/photos/diskfull": status_diskfull,
    "/photos/keepalive": status_keepalive,
    "/photos/fivelines": status_fivelines,
    "/photos/cls": status_cls,
    "/photos/show_mode": null_handler,
    "/photos/indexfile": null_handler,
  };

  const handler = handlers[topic];
  if (handler) {
    let parsedData = data;
    if (typeof data === "string") {
      try {
        parsedData = JSON.parse(data);
      } catch (err) {
        console.error(`Failed to parse JSON for topic ${topic}:`, err);
        // fall back to original string if parsing fails
        parsedData = data;
      }
    }
    handler(topic, parsedData);
  } else {
    console.error(`Unhandled topic: ${topic}`);
  }
}
