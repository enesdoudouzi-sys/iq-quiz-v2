package com.enesdoudouzi.iqtest;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;
import com.enesdoudouzi.iqtest.samsungiap.SamsungIapPlugin;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(SamsungIapPlugin.class);
        super.onCreate(savedInstanceState);
    }
}
