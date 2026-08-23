package com.enesdoudouzi.iqtest.samsungiap;

import android.util.Log;

import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.samsung.android.sdk.iap.lib.helper.HelperDefine;
import com.samsung.android.sdk.iap.lib.helper.IapHelper;
import com.samsung.android.sdk.iap.lib.listener.OnConsumePurchasedItemsListener;
import com.samsung.android.sdk.iap.lib.listener.OnGetOwnedListListener;
import com.samsung.android.sdk.iap.lib.listener.OnGetProductsDetailsListener;
import com.samsung.android.sdk.iap.lib.listener.OnPaymentListener;
import com.samsung.android.sdk.iap.lib.vo.ConsumeVo;
import com.samsung.android.sdk.iap.lib.vo.ErrorVo;
import com.samsung.android.sdk.iap.lib.vo.OwnedProductVo;
import com.samsung.android.sdk.iap.lib.vo.ProductVo;
import com.samsung.android.sdk.iap.lib.vo.PurchaseVo;

import java.util.ArrayList;

@CapacitorPlugin(name = "SamsungIap")
public class SamsungIapPlugin extends Plugin {

    private static final String TAG = "SamsungIapPlugin";
    private IapHelper iapHelper;

    @Override
    public void load() {
        super.load();
        iapHelper = IapHelper.getInstance(getContext());
    }

    @PluginMethod
    public void setOperationMode(PluginCall call) {
        String mode = call.getString("mode", "production");
        switch (mode) {
            case "test":
                iapHelper.setOperationMode(HelperDefine.OperationMode.OPERATION_MODE_TEST);
                break;
            case "test_failure":
                iapHelper.setOperationMode(HelperDefine.OperationMode.OPERATION_MODE_TEST_FAILURE);
                break;
            default:
                iapHelper.setOperationMode(HelperDefine.OperationMode.OPERATION_MODE_PRODUCTION);
                break;
        }
        call.resolve();
    }

    @PluginMethod
    public void getProductsDetails(PluginCall call) {
        String productIds = call.getString("productIds", "");
        iapHelper.getProductsDetails(productIds, new OnGetProductsDetailsListener() {
            @Override
            public void onGetProducts(ErrorVo errorVo, ArrayList<ProductVo> productList) {
                if (errorVo == null || errorVo.getErrorCode() != IapHelper.IAP_ERROR_NONE) {
                    call.reject("Samsung IAP Fehler: " + (errorVo != null ? errorVo.getErrorString() : "unbekannt"));
                    return;
                }
                JSArray arr = new JSArray();
                if (productList != null) {
                    for (ProductVo p : productList) {
                        JSObject o = new JSObject();
                        o.put("itemId", p.getItemId());
                        o.put("itemName", p.getItemName());
                        o.put("itemPrice", p.getItemPrice());
                        o.put("itemPriceString", p.getItemPriceString());
                        o.put("itemDesc", p.getItemDesc());
                        o.put("itemType", p.getItemType());
                        arr.put(o);
                    }
                }
                JSObject ret = new JSObject();
                ret.put("products", arr);
                call.resolve(ret);
            }
        });
    }

    @PluginMethod
    public void startPayment(PluginCall call) {
        String itemId = call.getString("itemId");
        if (itemId == null || itemId.isEmpty()) {
            call.reject("itemId fehlt");
            return;
        }
        iapHelper.startPayment(itemId, null, true, new OnPaymentListener() {
            @Override
            public void onPayment(ErrorVo errorVo, PurchaseVo purchaseVo) {
                if (errorVo == null || errorVo.getErrorCode() != IapHelper.IAP_ERROR_NONE) {
                    JSObject ret = new JSObject();
                    ret.put("success", false);
                    ret.put("errorCode", errorVo != null ? errorVo.getErrorCode() : -1);
                    ret.put("errorString", errorVo != null ? errorVo.getErrorString() : "unbekannt");
                    call.resolve(ret);
                    return;
                }
                JSObject ret = new JSObject();
                ret.put("success", true);
                ret.put("itemId", purchaseVo.getItemId());
                ret.put("purchaseId", purchaseVo.getPurchaseId());
                ret.put("purchaseDate", purchaseVo.getPurchaseDate());
                ret.put("itemType", purchaseVo.getItemType());
                call.resolve(ret);
            }
        });
    }

    @PluginMethod
    public void getOwnedList(PluginCall call) {
        String productType = call.getString("productType", "item");
        String type = "item".equals(productType) ? IapHelper.PRODUCT_TYPE_ITEM : IapHelper.PRODUCT_TYPE_ALL;
        iapHelper.getOwnedList(type, new OnGetOwnedListListener() {
            @Override
            public void onGetOwnedProducts(ErrorVo errorVo, ArrayList<OwnedProductVo> ownedList) {
                if (errorVo == null || errorVo.getErrorCode() != IapHelper.IAP_ERROR_NONE) {
                    call.reject("Samsung IAP Fehler: " + (errorVo != null ? errorVo.getErrorString() : "unbekannt"));
                    return;
                }
                JSArray arr = new JSArray();
                if (ownedList != null) {
                    for (OwnedProductVo o : ownedList) {
                        JSObject item = new JSObject();
                        item.put("itemId", o.getItemId());
                        item.put("purchaseId", o.getPurchaseId());
                        item.put("purchaseDate", o.getPurchaseDate());
                        arr.put(item);
                    }
                }
                JSObject ret = new JSObject();
                ret.put("owned", arr);
                call.resolve(ret);
            }
        });
    }

    @PluginMethod
    public void consumePurchasedItems(PluginCall call) {
        String purchaseId = call.getString("purchaseId");
        if (purchaseId == null || purchaseId.isEmpty()) {
            call.reject("purchaseId fehlt");
            return;
        }
        iapHelper.consumePurchasedItems(purchaseId, new OnConsumePurchasedItemsListener() {
            @Override
            public void onConsumePurchasedItems(ErrorVo errorVo, ArrayList<ConsumeVo> consumeList) {
                if (errorVo == null || errorVo.getErrorCode() != IapHelper.IAP_ERROR_NONE) {
                    call.reject("Samsung IAP Fehler: " + (errorVo != null ? errorVo.getErrorString() : "unbekannt"));
                    return;
                }
                call.resolve();
            }
        });
    }
}
