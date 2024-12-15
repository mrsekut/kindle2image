use core_foundation::array::CFArray;
use core_foundation::base::{CFTypeRef, TCFType};
use core_foundation::dictionary::CFDictionary;
use core_foundation::string::CFString;
use core_graphics::window::{kCGWindowListOptionOnScreenOnly, CGWindowListCopyWindowInfo};

fn main() {
    unsafe {
        // 画面上のすべてのウィンドウ情報を取得
        let window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, 0);

        if window_list.is_null() {
            println!("ウィンドウリストを取得できませんでした。");
            return;
        }

        // CFArray型にキャスト
        let windows: CFArray<CFDictionary<CFString, CFTypeRef>> =
            CFArray::wrap_under_get_rule(window_list);

        println!("ウィンドウの数: {}", windows.len());

        for (i, window) in windows.iter().enumerate() {
            // CFDictionaryを操作する
            if let Some(name) = get_string_from_dict(&window, "kCGWindowName") {
                println!("ウィンドウ {} の名前: {}", i, name);
            }
        }
    }
}

// /// CFDictionaryから指定したキーの値を取得し、RustのStringに変換
// fn get_string_from_dict(dict: &CFDictionary<CFString, CFTypeRef>, key: &str) -> Option<String> {
//     let cf_key = CFString::from_static_string(key);
//     let value = dict.find(&cf_key)?;

//     // CFTypeRefをCFStringにキャスト
//     if value.is_null() {
//         return None;
//     }
//     let cf_string: CFString = unsafe { CFString::wrap_under_get_rule(value as *const _) };
//     Some(cf_string.to_string())
// }
