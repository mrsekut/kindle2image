use core_foundation::array::CFArray;
use core_foundation::base::{CFTypeRef, TCFType, TCFTypeRef};
use core_foundation::dictionary::CFDictionary;
use core_foundation::string::CFString;
use core_graphics::window::{kCGWindowListOptionOnScreenOnly, CGWindowListCopyWindowInfo};

fn main() {
    unsafe {
        // 画面上のすべてのウィンドウ情報を取得
        let window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, 0);
        let windows: CFArray<CFDictionary<CFString, CFTypeRef>> =
            CFArray::wrap_under_get_rule(window_list);

        windows.iter().for_each(|window| {
            if let Some(name) = get_string_from_dict(&window, "kCGWindowName") {
                println!("ウィンドウの名前: {}", name);
            }

            if let Some(owner) = get_string_from_dict(&window, "kCGWindowOwnerName") {
                println!("ウィンドウのオーナー: {}", owner);
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
