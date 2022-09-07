#include "MyOtherTestingClass.h"

#include <chrono>

#ifdef CPlusPlusCode
namespace a {
namespace b {
class Hallo;
namespace c {
class World;
}
}
}

enum class MyEnum
{
	VALUE_0,
	VALUE_1
};

using MyFancyFn = std::function<bool(int*)>;

typedef std::pair<double, int> MyPair;

#endif

const unsigned HELLO_1 = 1;
const unsigned HELLO_2 = 2;

class MyForwardDeclaration;

std::ostream& operator<<(std::ostream& os, TestExampleClass& asset);

class TestExampleClass : public BaseTestClass
{
  public:
	friend class MyGoodFriend;

	Unsafe int createArray(const date& theDate,
	                                    const date& otherDate,
	                                    long hello,
	                                    array* theArray);

	Nowrapper int getArray(const date* theDate,
	                                  const AmisDate* otherDate,
	                                  array* theArray,
	                                  long type = 0,
	                                  date* oneMoreDate = nullptr,
	                                  bool aBoolean= false);
	virtual int getSomething(
	  array* theArray);

	double getSomethingElse(int i = C42);

	virtual const abc::def::foo& getFancyThing() const;
	static long getMoreStuff(bool theBool);

	flags flags() const;

	void setFlags(const flags& f);

	Hello* hello;

	bool isFSomethingTrue();

	double someBool;

	BigThing reallyBig;
};
