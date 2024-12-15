use core_foundation::array::CFArray;
use core_foundation::base::{CFTypeRef, TCFType, TCFTypeRef};
use core_foundation::dictionary::CFDictionary;
use core_foundation::number::CFNumber;
use core_foundation::string::CFString;
use core_graphics::window::{kCGWindowListOptionOnScreenOnly, CGWindowListCopyWindowInfo};

#[derive(Debug)]
#[allow(dead_code)]
pub struct WindowPosition {
    x: f64,
    y: f64,
    width: f64,
    height: f64,
}

pub fn get_window_position(name: &str) -> Option<WindowPosition> {
    unsafe {
        let window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, 0);
        let windows: CFArray<CFDictionary<CFString, CFTypeRef>> =
            CFArray::wrap_under_get_rule(window_list);

        return windows
            .iter()
            .filter_map(|window| extract_bounds_if_name_matches(&window, name))
            .map(|bounds| WindowPosition {
                x: get_number_from_dict(&bounds, "X").unwrap_or(0.0),
                y: get_number_from_dict(&bounds, "Y").unwrap_or(0.0),
                width: get_number_from_dict(&bounds, "Width").unwrap_or(0.0),
                height: get_number_from_dict(&bounds, "Height").unwrap_or(0.0),
            })
            .next();
    }
}

fn extract_bounds_if_name_matches(
    window: &CFDictionary<CFString, CFTypeRef>,
    name: &str,
) -> Option<CFDictionary<CFString>> {
    get_string_from_dict(&window, "kCGWindowOwnerName")
        .filter(|owner| owner == name)
        .and_then(|_| get_dict_from_dict(&window, "kCGWindowBounds"))
}

fn get_string_from_dict(dict: &CFDictionary<CFString, CFTypeRef>, key: &str) -> Option<String> {
    let cf_key = CFString::new(key);
    let value_ref = dict.find(&cf_key)?;
    let value_ptr = value_ref.as_void_ptr();

    if value_ptr.is_null() {
        return None;
    }

    let cf_string: CFString = unsafe { CFString::wrap_under_get_rule(value_ptr as *const _) };

    Some(cf_string.to_string())
}

fn get_number_from_dict(dict: &CFDictionary<CFString, CFTypeRef>, key: &str) -> Option<f64> {
    let cf_key = CFString::new(key);
    let value_ref = dict.find(&cf_key)?;
    let value_ptr = value_ref.as_void_ptr();

    let cf_number = unsafe { CFNumber::wrap_under_get_rule(value_ptr as *const _) };

    cf_number.to_f64()
}

fn get_dict_from_dict(
    dict: &CFDictionary<CFString, CFTypeRef>,
    key: &str,
) -> Option<CFDictionary<CFString, CFTypeRef>> {
    let cf_key = CFString::new(key);
    let value_ref = dict.find(&cf_key)?;
    let value_ptr = value_ref.as_void_ptr();

    if value_ptr.is_null() {
        return None;
    }

    unsafe { Some(CFDictionary::wrap_under_get_rule(value_ptr as *const _)) }
}
