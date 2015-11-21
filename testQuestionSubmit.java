package cityquizdb;

import java.util.regex.Pattern;
import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;
import static org.hamcrest.CoreMatchers.*;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;

public class TestQuestionSubmit {
	private WebDriver driver;
	private String baseUrl;
	private boolean acceptNextAlert = true;
	private StringBuffer verificationErrors = new StringBuffer();

	@Before
	public void setUp() throws Exception {
		driver = new FirefoxDriver();
		baseUrl = "http://www.cityquizsubmit.appspot.com/";
		driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
	}

	@Test
	//tests that the login works and question submission works
	public void testQuestionSubmit() throws Exception {
		driver.get(baseUrl + "/");
		driver.findElement(By.id("username")).clear();
		driver.findElement(By.id("username")).sendKeys("DannyA");
		driver.findElement(By.id("password")).clear();
		driver.findElement(By.id("password")).sendKeys("123");
		driver.findElement(By.id("loginsubmit")).click();
		new Select(driver.findElement(By.id("catagories"))).selectByVisibleText("Business");
		driver.findElement(By.id("questionbox")).clear();
		driver.findElement(By.id("questionbox")).sendKeys("test");
		driver.findElement(By.id("answer1")).clear();
		driver.findElement(By.id("answer1")).sendKeys("1");
		driver.findElement(By.id("answer2")).clear();
		driver.findElement(By.id("answer2")).sendKeys("2");
		driver.findElement(By.id("answer3")).clear();
		driver.findElement(By.id("answer3")).sendKeys("3");
		driver.findElement(By.id("answer4")).clear();
		driver.findElement(By.id("answer4")).sendKeys("4");
		driver.findElement(By.cssSelector("input[type=\"submit\"]")).click();
		String URL = driver.getCurrentUrl();
		assertEquals(URL, "http://www.cityquizsubmit.appspot.com/savePost");
	}

	@After
	public void tearDown() throws Exception {
		driver.quit();
		String verificationErrorString = verificationErrors.toString();
		if (!"".equals(verificationErrorString)) {
			fail(verificationErrorString);
		}
	}

	private boolean isElementPresent(By by) {
		try {
			driver.findElement(by);
			return true;
		} catch (NoSuchElementException e) {
			return false;
		}
	}

	private boolean isAlertPresent() {
		try {
			driver.switchTo().alert();
			return true;
		} catch (NoAlertPresentException e) {
			return false;
		}
	}

	private String closeAlertAndGetItsText() {
		try {
			Alert alert = driver.switchTo().alert();
			String alertText = alert.getText();
			if (acceptNextAlert) {
				alert.accept();
			} else {
				alert.dismiss();
			}
			return alertText;
		} finally {
			acceptNextAlert = true;
		}
	}
}
