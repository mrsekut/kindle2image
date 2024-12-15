use core_foundation::array::CFArray;
use core_foundation::base::{CFTypeRef, TCFType, TCFTypeRef};
use core_foundation::dictionary::CFDictionary;
use core_foundation::number::CFNumber;
use core_foundation::string::CFString;
use core_graphics::window::{kCGWindowListOptionOnScreenOnly, CGWindowListCopyWindowInfo};

fn main() {
    unsafe {
        // 画面上のすべてのウィンドウ情報を取得
        let window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, 0);
        let windows: CFArray<CFDictionary<CFString, CFTypeRef>> =
            CFArray::wrap_under_get_rule(window_list);

        // TODO: func:arg:kindle
        windows.iter().for_each(|window| {
            if let Some(owner) = get_string_from_dict(&window, "kCGWindowOwnerName") {
                if owner == "Kindle" {
                    if let Some(bounds) = get_dict_from_dict(&window, "kCGWindowBounds") {
                        dbg!(&bounds);
                        let x = get_number_from_dict(&bounds, "X").unwrap_or(0.0);
                        let y = get_number_from_dict(&bounds, "Y").unwrap_or(0.0);
                        let width = get_number_from_dict(&bounds, "Width").unwrap_or(0.0);
                        let height = get_number_from_dict(&bounds, "Height").unwrap_or(0.0);

                        println!(
                            "Kindleウィンドウの座標: X: {}, Y: {}, 幅: {}, 高さ: {}",
                            x, y, width, height
                        );
                    }
                }
            }
        });
    }
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
    let cf_number = unsafe { CFNumber::wrap_under_get_rule(value_ref.as_void_ptr() as *const _) };

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
