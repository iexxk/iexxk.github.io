---
title: EasyUi的使用
date: 2017-12-14 18:33:27
categories: JavaEE
tags: [jsp,EasyUi,ComboBox]
---
### [EasyUi Demo](https://www.jeasyui.com/demo/main/index.php)

#### ComboBox自定义多选下拉加模糊搜索的功能

1. 添加控件引用

```jsp
<tr>
    <th>多选模糊搜素</th>
    <td>
        <select id="comboboxid" name="comboboxname" class="easyui-combobox" placeholder="aa" multiline="true" data-options="required:false,prompt:'不选默认为全部'" style="width:228px;height: 29px;"></select>
    </td>
</tr>
```

其中`prompt:'不选默认为全部'`为背景提示语，`multiline="true"`为控件显示多行滚动条

2. 在`<script type="text/javascript"></script>`添加js功能代码

```js
$(function() {
var lent=0;
$('#comboboxid').combobox({
      url:'${pageContext.request.contextPath}/invitationCodeController/tree?checkAuthority=1',
      multiple:true,
      valueField:'invatationcode',
      textField: 'invatationcode',
      value: '${setInvitationCodes}',
      onBeforeLoad:function(param){
          console.log("user",'${user.getMemberUnitId()}');
          param.memberUnitId='${user.getMemberUnitId()}';
          console.log("param",param);
      },
      formatter: function (row) {
          row.codeRemark= row.invatationcode+"("+row.remark+")";
          return  row.codeRemark;
      },
      filter:function(q,row){
          return row.codeRemark.indexOf(q)!=-1;
      },
      onSelect: function (row) {
          console.log("onSelect",row);
          var values=$(this).combobox('getValues');
          var getData=$(this).combobox('getData');
          console.log("getdata",getData);
          var valuesT=[];
          for(i=0;i<values.length;i++){
             for (ii=0;ii<getData.length;ii++){
                 if (values[i]==getData[ii].invatationcode){
                     valuesT.push(values[i]);
                     console.log("有效",valuesT);
                 }
             }
          }
          if (lent==valuesT.length-1){
              console.log("==");
              lent= valuesT.length;
              $(this).combobox('setValues',valuesT);
          }else {
              console.log("!=")
          }
      }
  });
});
```

数据请求设置` url:'${pageContext.request.contextPath}/invitationCodeController/tree?checkAuthority=1',`

参数设置,其中`'${user.getMemberUnitId()}'`是从java后端传过来，等于`&memberUnitId=${user.getMemberUnitId()}'`

```js
      onBeforeLoad:function(param){
          console.log("user",'${user.getMemberUnitId()}');
          param.memberUnitId='${user.getMemberUnitId()}';
          console.log("param",param);
      },
```

`  valueField:'invatationcode', textField: 'invatationcode',`一个id一个展示的值，展示的值通过`formatter`自定义，显示样式为`27490008(测试)`

```js
  formatter: function (row) {
          row.codeRemark= row.invatationcode+"("+row.remark+")";
          return  row.codeRemark;
      },
```

` value: '${setInvitationCodes}',`这句设置是从java后端获取出数值，默认选择或加载的值，在输入框会显示该值

设置模糊搜索，通过过滤函数`filter`意思是row中包含q查询参数就显示

```js
      filter:function(q,row){
          return row.codeRemark.indexOf(q)!=-1;
      },
```

上面设置完了模糊搜索加多选是实现了，但是输入的模糊查找的字符不会自动去掉，下面设置

```js
      onSelect: function (row) {
          console.log("onSelect",row);
          var values=$(this).combobox('getValues');
          var getData=$(this).combobox('getData');
          console.log("getdata",getData);
          var valuesT=[];
          for(i=0;i<values.length;i++){
             for (ii=0;ii<getData.length;ii++){
                 if (values[i]==getData[ii].invatationcode){
                     valuesT.push(values[i]);
                     console.log("有效",valuesT);
                 }
             }
          }
          if (lent==valuesT.length-1){
              console.log("==");
              lent= valuesT.length;
              $(this).combobox('setValues',valuesT);
          }else {
              console.log("!=")
          }
      }
```

通过遍历源数据`  var getData=$(this).combobox('getData');`和选中的数据（输入框的数据）` var values=$(this).combobox('getValues');`对比得到有效的选中数据，但是还需要在合适的时间设置有效选择数据

`onSelect`方法在输入框输入字和选择时都会触发，因此加个判断`if (lent==valuesT.length-1)`当选中有效数据每增加1个时触发因此比较长度即可，`lent`为全局变量，做历史长度存储

数据返回json格式

```json
[
    {
        "invatationcode": "27491007", 
        "createdate": 1510284005000, 
        "updatedate": 1510284005000, 
        "flag": 1, 
        "remark": "我是账号备注"
    },
  .........
    {
        "invatationcode": "27490008", 
        "createdate": 1510284334000, 
        "updatedate": 1510284334000, 
        "flag": 1, 
        "remark": "测试", 
    }
]
```

