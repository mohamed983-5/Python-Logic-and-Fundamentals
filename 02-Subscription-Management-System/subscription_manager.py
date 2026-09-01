class Member:
    def __init__(self, name, age, member_ship):
        if not isinstance(name, str) or str(name).isdigit():
            raise ValueError("Invalid name")
        if not isinstance(age, int) or age < 16:
            raise ValueError("Invalid age")
        self.name = name
        self.age = age
        self.member_ship = member_ship

    names = {}  # noqa: RUF012
    total_members = 0

    @classmethod
    def get_total_members(cls):
        return cls.total_members

    @classmethod
    def get_all_members(cls):
        return cls.names.copy()


class BasicMember(Member):
    price = 200

    def __init__(self, name, age, member_ship):
        super().__init__(name, age, member_ship)
        Member.total_members += 1

    def add_member(self):
        Member.names[self.name] = {
            "age": self.age,
            "membership": self.member_ship,
            "price": self.price,
            "type": "Basic"
        }
        print(f"✓ {self.name} added as Basic Member")


class PremiumMember(Member):
    price = 500

    def __init__(self, name, age, member_ship):
        super().__init__(name, age, member_ship)
        Member.total_members += 1

    def add_member(self):
        Member.names[self.name] = {
            "age": self.age,
            "membership": self.member_ship,
            "price": self.price,
            "type": "Premium"
        }
        print(f"✓ {self.name} added as Premium Member")


def main():
    while True:
        print("\n=== Subscription Menu ===")
        print("1 - Add Subscription")
        print("2 - View All Members")
        print("3 - Exit")
        
        try:
            choice = input("Please enter number: ").strip()
            
            if choice == "1":
                membership_type = input("Choose subscription (premium/basic): ").lower().strip()
                
                if membership_type not in ["premium", "basic"]:
                    print("✗ Invalid subscription type")
                    continue
                
                name = input("Enter your name: ").strip()
                age_input = input("Enter your age: ").strip()
                membership = input("Enter your membership details: ").strip()
                
                try:
                    age = int(age_input)
                    
                    if membership_type == "premium":
                        member = PremiumMember(name, age, membership)
                        member.add_member()
                    else:
                        member = BasicMember(name, age, membership)
                        member.add_member()
                        
                except ValueError as e:
                    print(f"✗ Error: {e}")
                    
            elif choice == "2":
                if Member.names:
                    print(f"\n=== All Members (Total: {Member.get_total_members()}) ===")
                    for name, details in Member.names.items():
                        print(f"  {name}: {details}")
                else:
                    print("✗ No members added yet")
                    
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("✗ Invalid choice")
                
        except KeyboardInterrupt:
            print("\nProgram terminated")
            break
        except Exception as e:  # noqa: BLE001
            print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
