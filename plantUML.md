@startuml
class Customers {
  CustomerId
  Name
  Address

}

class Orders {
  OrderId
  OrderDate
  DeliveryDate

}

class OrderedProductQnt << weak >>{
  ProductQuantity

}

class Products{
  Product_name

}

class Reciepes << weak >> {
  Quantity
  Unit

}

class Ingredients {
  Ingredients_Name
  QuantityStorage
  LastDeliveryTime
  LastDeliveryQuantity

}

class Pallets {
  PalletId
  ProductionDate
  DateDelivered
  BlockedStatus
  CurrentLocation

}



Customers "1" -- "*" Orders

Products"*" -- "*" Orders
(Products, Orders) .. OrderedProductQnt


Products "*" -- "*" Ingredients
(Products, Ingredients) .. Reciepes 
Products "1" -- "*" Pallets
Orders"0,1" -- "*" Pallets
@enduml